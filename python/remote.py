import logging
import time
import socket
import os
import paramiko
import re
import sys
import select
import uuid

from threading import Lock

from cmsqalib.config import Logger, MachineInfo, TestConfigurationManager
from cmsqalib.cmexceptions import SshException
from cmsqalib.util.fileutil import LocalFileUtil
from cmsqalib.util.stringutil import StringUtils

log = Logger.Instance().getLogger()
logging.getLogger('paramiko').setLevel(logging.WARNING)


def db_retry(func):
    def retry_decor(*args, **kwargs):
        retry_count = 1
        while retry_count <= 6:
            try:
                return func(*args, **kwargs)
            except DatabaseLockedError as ex:
                if retry_count > 5:
                    raise ex
                log.warning('sleep 2 seconds before retrying command....')
                time.sleep(2)
                retry_count += 1
    return retry_decor


# Helper. Read a file and return list with lines as elements.
# Remove symbol '\n' at the end of line
def to_list_from_file(fn):
    with open(fn) as f:
        return [ln[:-1] for ln in f if ln.endswith('\n')]


class RemoteConstants:
    DB_LOCKED_EMSG = 'database is locked'
    SLEEP_DELAY = 0.5
    STDOUT_TIMEOUT = 60 * 15    # 10 minutes
    CMD_TIMEOUT = 60 * 25       # 25 minutes


class DatabaseLockedError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SshTimeout(Exception):

    """ Exception class for timeouts durring SSH operations """

    def __init__(self, message="Remote operation timeout"):
        """
        Constructor for the SSH Timeout Exception class
        @param message: User defined error message.
        """
        super(SshTimeout, self).__init__(message)


class RemoteOperation(object):

    @classmethod
    def _posix_shell(cls, chan, user_input, iotimeout, iodelay, cmcli_bool):
        """
        Interactively send commands to an interactive shell

        Input:
        chan: The paramiko channel
        user_input: The input to send to the interactive shell
        iotimeout: Timeout variable to wait for stdout for a given select
        iodelay: time to wait before sending input
        cmcli_bool: Toggle cmcli vs bash command line operations
        """
        timeout = 60  # 1 mins , only its only applicable to cmcli ssl commands
        result = ''
        input = list(user_input)
        cmcli_ssl_bool = False
        last_prompt = ''
        if len(filter(lambda x: x.find('ssl') >= 0, user_input)) > 0:
            cmcli_ssl_bool = True
        if cmcli_bool:
            input_end = 1
        else:
            input_end = 0
        try:
            iotimeout_save = chan.gettimeout()
            chan.settimeout(iotimeout)
            input.reverse()
            start_time = time.time()

            while True:
                # we dont need this hack this is only happenning for ssl tests
                if cmcli_ssl_bool and time.time() - start_time > timeout:
                    log.error('time to break out of the loop.waited %s seconds' % timeout)
                    raise OSError('Remote Command timeout after {} seconds'.format(timeout))
                log.debug('Running select')
                r, w, e = select.select([chan, sys.stdin], [], [], 5)
                log.debug('select done')

                log.debug('r: %s' % repr(r))
                log.debug('w: %s' % repr(w))
                log.debug('e: %s' % repr(e))

                if chan in r:
                    log.debug('rlist: wait until ready for reading')
                    try:
                        log.debug('channel receiving data')

                        # Start with something
                        x = "DO IT"
                        while len(x) > 0:

                            # Got stuff. Print it
                            time.sleep(iodelay)
                            log.debug('get some data')
                            x = chan.recv(20480)
                            last_prompt = x
                            result += x
                            log.debug('data received. Write it to stdout')
                            sys.stdout.write(x)
                            log.debug('flushing stdout')
                            sys.stdout.flush()

                            # We've sent it all. Let's get out
                            if len(input) == input_end:
                                log.debug('NOTHING LEFT TO SEND')
                                raise

                            # Program exited too soon
                            if chan.exit_status_ready():
                                log.warn('Hit exit status ready sooner than expected')
                                chan.send('\n')
                                raise

                    except socket.timeout:
                        log.debug('All stdout exhausted')
                        if len(input) > input_end:
                            x = input.pop()
                            log.debug('SENDING to input stream: %s' % x)
                            chan_in = '%s\n' % x
                            chan.send(chan_in)
                            result += chan_in
                        else:
                            if chan.exit_status_ready():
                                log.info('Program ready to exit')
                                break

                            # Keep reading for cmcli commands since we need to
                            # wait until we get back to the prompt
                            if not cmcli_bool:
                                log.debug('Break out of select loop')
                                break
                            elif last_prompt and last_prompt.lower().find('cryptomanager>') >= 0:
                                log.debug('Cryptomanager prompt is seen')
                                break
                        pass

                if not r:
                    # FIXME: I think we want to inspect the the last prompt.
                    # If it was input, we should probably attempt another select
                    # if we are running a cmcli command
                    log.debug("Nothing to send or unexpected prompt. " +
                              "Prompt was: %s" % last_prompt)
                    raise

        finally:

            # Assume the last input is logout
            if cmcli_bool:
                x = input.pop()
                log.debug('SENDING logout to input stream: %s' % x)
                chan_in = '%s\n' % x
                chan.send(chan_in)
                result += chan_in

            log.debug('Trying to get exit status for command')
            exit_status = chan.recv_exit_status()
            log.debug('Got exit status for command: %s', exit_status)
            x = chan.recv(20480)
            log.debug("Last data received: %s" % x)
            result += x
            sys.stdout.write(x)
            sys.stdout.flush()
            log.debug("return from posix shell")
            chan.settimeout(iotimeout_save)
            return result, exit_status

    @classmethod
    def run_interactive(cls, shell, command, input, iotimeout, iodelay):

        remote_host = 'unknown'
        error = list()
        stderro = shell.makefile_stderr('rb')

        try:
            remote_host = socket.gethostbyaddr(shell.getpeername()[0])[0].split('.')[0]
        except socket.herror:
            remote_host = shell.getpeername()[0]

        log.info('%s: Executing command: %s' % (remote_host, command))
        log.info('%s: iotimeout: %s iodelay: %s: Command parameters: %s'
                 % (remote_host, iotimeout, iodelay, input))
        shell.get_pty()
        shell.exec_command(command)
        if 'cmcli' in command:
            result, exit_status = cls._posix_shell(shell, input, iotimeout, iodelay, True)
        else:
            result, exit_status = cls._posix_shell(shell, input, iotimeout, iodelay, False)
        log.debug('%s: Done attempting to execute command: %s' % (remote_host, command))

        error = stderro.read()
        if stderro:
            stderro.close()

        # FIXME: This causes the output to get into the log files but also
        # causes duplicate output on the console. Need to fix that.
        if result:
            log.info('%s: Result:\n%s' % (remote_host, result))

        # FIXME: I'm also positive we want to check result in all cases and just
        # remove error completely
        if exit_status:
            log.debug('%s: Do somthing with exit status' % (remote_host))
            if (re.search(r"Could not convert (.*) to a numeric value", result)
                    or re.search(r"\n\n\n", result)
                    or "Action cancelled on user request" in error
                    or "Password len of " in error):
                return result
            log.warning('%s: Command failed: %s : RC %i' % (remote_host, command, exit_status))
            # This is needed for negative tests, where the stderr does not contain any data
            if error is '':
                err_str = result
            else:
                err_str = error
            raise SshException('%s: %s' % (remote_host, err_str))

        log.debug('%s: Command Executed successfully: %s : RC %i' % (remote_host, command, exit_status))

        return result

    @classmethod
    def upload(cls, sftp, source, destination):
        remote_host = 'unknown'
        fileutil = LocalFileUtil()
        try:
            remote_host = socket.gethostbyaddr(sftp.get_channel().getpeername()[0])[0].split('.')[0]
        except socket.herror:
            remote_host = sftp.get_channel().getpeername()[0]

        if not fileutil.is_file(source):
            err_msg = "Source file given not there: %s" % (source)
            log.error(err_msg)
            raise OSError(err_msg)

        try:
            log.info('Uploading %s to %s:%s' % (source, remote_host, destination))
            sftp.put(source, destination)
            log.debug('Upload succeeded')
        except Exception as ex:
            log.error("%s" % (repr(ex)))
            raise SshException(ex.message)

        return True

    @classmethod
    def download(cls, sftp, source, destination, print_to_console=True):
        remote_host = 'unknown'
        try:
            remote_host = socket.gethostbyaddr(sftp.get_channel().getpeername()[0])[0].split('.')[0]
        except socket.herror:
            remote_host = sftp.get_channel().getpeername()[0]

        try:
            if print_to_console:
                log.info('Downloading from %s:%s to %s' % (remote_host, source,
                                                           destination))
            sftp.get(source, destination)
            log.debug('Download succeeded')
        except IOError as ex:
            log.warning('Could not open file {} on device {}'.format(source, remote_host))
            raise IOError(ex)
        except Exception as ex:
            log.error("%s" % (repr(ex)))
            raise SshException(ex.message)

        return True

    @classmethod
    def run(cls, shell, command, exit_if_error=True, log_error_as_warning=False,
            print_to_console=True):
        remote_host = 'unknown'
        output = list()
        error = list()
        temp = ''
        stdout = shell.makefile('rb', -1)
        stderro = shell.makefile_stderr('rb', -1)
        try:
            remote_host = socket.gethostbyaddr(shell.getpeername()[0])[0].split('.')[0]
        except socket.herror:
            remote_host = shell.getpeername()[0]

        if print_to_console:
            log.info('%s: Executing command: %s' % (remote_host, command))
        if command.find('sudo') >= 0:
            shell.get_pty()
        shell.exec_command(command)

        # Timeout handling
        initial_time = time.time()
        while not shell.exit_status_ready():
            duration = time.time() - initial_time

            # We close the stdout channel if we find that the command error.
            # We do this to prevent hanging while waiting for stdout to get EOF
            # due to a large stderr stream. The error messages will be logged
            # below in the error handling section of this method
            if duration > RemoteConstants.STDOUT_TIMEOUT \
                    and (stderro.channel.eof_received or shell.recv_stderr_ready()):
                log.warning('Found errors after {} seconds.'.format(duration))
                msg = 'Taking the errors we got and forcefully closing the stdout channel.'
                log.warning(msg)
                stdout.channel.close()
                break

            # Kill the session if the command does not return after a long time
            # regardless of the fact no errors were detected during execution
            if duration > RemoteConstants.CMD_TIMEOUT:
                msg = 'Timeout after {} seconds. Aborting remote op'.format(duration)
                log.warning(msg)
                raise SshTimeout(msg)

            time.sleep(RemoteConstants.SLEEP_DELAY)

        log.debug('{}: Reading stdout: {}'.format(remote_host, repr(stdout)))
        for line in stdout:
            log.debug('{}: Reading line: {}'.format(remote_host, line))
            output.append(line.rstrip())
        if output and print_to_console:
            log.info('{}: Output: {}'.format(remote_host, '\n'.join(output)))

        log.debug('%s: Running: stderro.read()' % remote_host)
        error = stderro.read()
        log.debug('error: {}'.format(repr(error)))
        log.debug('%s: Done: stderro.read()' % remote_host)

        log.debug('%s: Running: shell.recv_exit_status()' % remote_host)
        exit_status = shell.recv_exit_status()
        log.debug('{}: Done: shell.recv_exit_status() : RC : {}'.format(
            remote_host, exit_status))

        if stdout:
            stdout.close()
        if stderro:
            stderro.close()

        # FIXME: We'll want to move this up higher up in the method body later
        status_dict = {
            'rhost': remote_host,
            'cmd': command,
            'ret_code': exit_status,
            'emsg': error,
            'short_emsg': StringUtils.truncate_string(error),
        }

        if exit_status and exit_if_error:
            msg = '{rhost}: Command failed: {cmd} : RC {ret_code}'.format(**status_dict)
            log.warning(msg)

            ex_msg = 'command: {cmd} failed {rhost}: {short_emsg}'.format(**status_dict)

            if 'No such file or directory' in error:
                log.warning('{rhost}: Error message: {emsg}'.format(**status_dict))
                raise OSError(ex_msg)
            elif RemoteConstants.DB_LOCKED_EMSG in error:
                log.warning('{rhost}: DB lock: Error message: {emsg}'.format(**status_dict))
                raise DatabaseLockedError(RemoteConstants.DB_LOCKED_EMSG)
            elif error:
                emsg = '{rhost}: Error message: {emsg}'.format(**status_dict)
                if log_error_as_warning:
                    log.warning(emsg)
                else:
                    log.error(emsg)
            else:
                emsg = '{rhost}: Command failed but stderr was empty'.format(**status_dict)
                if log_error_as_warning:
                    log.warning(emsg)
                else:
                    log.error(emsg)
            raise SshException('{} , stdout : {}'.format(ex_msg, ''.join(output)))

        # FIXME: This should be logged at debug level
        msg = '{rhost}: Command Executed successfully: {cmd} : RC {ret_code}'.format(**status_dict)
        log.debug(msg)

        return output, error.splitlines()


class RemoteOperationBash(RemoteOperation):

    @classmethod
    def run_interactive(cls, shell, command, input):
        """
        Run interactive commands using bash tricks. This is good for simple ops
        """
        feed = '\\n'.join(input)
        icommand = "echo -e '{}' | {}".format(feed, command)
        _stdout, _stderr = cls.run(shell, icommand)
        return _stdout


class RemoteOperationRaw(RemoteOperation):

    @classmethod
    def _posix_shell(cls, chan, user_input, iotimeout, iodelay):
        """
        Interactively send commands to an interactive shell.
        IMPORTANT!!!
        This version of posix_shell does not automatically insert end of line
        characters, instead, these must be embedded in the user_input stream
        In certain cases, it has been learned the \r\n is required to terminate
        lines, as opposed to simply \n
        To use this version of RemoteOperation, ShellConnectorRaw needs to be used

        Input:
        chan: The paramiko channel
        user_input: The input to send to the interactive shell
        iotimeout: Timeout variable to wait for stdout for a given select
        iodelay: time to wait before sending input
        """
        timeout = 60  # 1 mins , only its only applicable to cmcli ssl commands
        result = ''
        input = list(user_input)
        input_end = 1
        try:
            chan.settimeout(iotimeout)
            input.reverse()
            start_time = time.time()

            while True:
                # we dont need this hack this is only happenning for ssl tests
                log.debug('Running select')
                r, w, e = select.select([chan, sys.stdin], [], [], 5)
                log.debug('select done')

                log.debug('r: %s' % repr(r))
                log.debug('w: %s' % repr(w))
                log.debug('e: %s' % repr(e))

                if chan in r:
                    log.debug('rlist: wait until ready for reading')
                    try:
                        log.debug('channel receiving data')

                        # Start with something
                        x = "DO IT"
                        while len(x) > 0:

                            # Got stuff. Print it
                            time.sleep(iodelay)
                            log.debug('get some data')
                            x = chan.recv(20480)
                            last_prompt = x
                            result += x
                            log.debug('data received. Write it to stdout')
                            sys.stdout.write(x)
                            log.debug('flushing stdout')
                            sys.stdout.flush()

                            # We've sent it all. Let's get out
                            if len(input) == input_end:
                                log.debug('NOTHING LEFT TO SEND')

                            # Program exited too soon
                            if chan.exit_status_ready():
                                log.warn('Hit exit status ready sooner than expected')
                                chan.send('^D\n')
                                raise

                    except socket.timeout:
                        log.debug('All stdout exhausted')
                        if len(input) > input_end:
                            x = input.pop()
                            log.debug('SENDING to input stream: %s' % x)
                            chan_in = '%s' % x
                            chan.send(chan_in)
                            result += chan_in
                        else:
                            if chan.exit_status_ready():
                                log.info('Program ready to exit')
                                break

                            # Keep reading for cmcli commands since we need to
                            # wait until we get back to the prompt
                        pass

                if not r:
                    # FIXME: I think we want to inspect the the last prompt.
                    # If it was input, we should probably attempt another select
                    # if we are running a cmcli command
                    log.debug("Nothing to send or unexpected prompt. " +
                              "Prompt was: %s" % last_prompt)
                    raise

        finally:

            # Assume the last input is logout
            x = input.pop()
            log.debug('SENDING logout to input stream: %s' % x)
            chan_in = '%s\n' % x
            chan.send(chan_in)
            result += chan_in

            log.debug('Trying to get exit status for command')
            exit_status = chan.recv_exit_status()
            log.debug('Got exit status for command: %s', exit_status)
            x = chan.recv(20480)
            log.debug("Last data received: %s" % x)
            result += x
            sys.stdout.write(x)
            sys.stdout.flush()
            log.debug("return from posix shell")
            return result, exit_status

    @classmethod
    def run_interactive(cls, shell, command, input, iotimeout, iodelay):

        remote_host = 'unknown'
        error = list()
        stderro = shell.makefile_stderr('rb')

        try:
            remote_host = socket.gethostbyaddr(shell.getpeername()[0])[0].split('.')[0]
        except socket.herror:
            remote_host = shell.getpeername()[0]

        log.info('%s: Executing command: %s' % (remote_host, command))
        log.info('%s: iotimeout: %s iodelay: %s: Command parameters: %s'
                 % (remote_host, iotimeout, iodelay, input))
        shell.get_pty()
        shell.exec_command(command)
        result, exit_status = cls._posix_shell(shell, input, iotimeout, iodelay)

        error = stderro.read()
        if stderro:
            stderro.close()

        # FIXME: This causes the output to get into the log files but also
        # causes duplicate output on the console. Need to fix that.
        if result:
            log.info('%s: Result:\n%s' % (remote_host, result))

        # FIXME: I'm also positive we want to check result in all cases and just
        # remove error completely
        if exit_status:
            log.debug('%s: Do somthing with exit status' % (remote_host))
            if (re.search(r"Could not convert (.*) to a numeric value", result)
                    or re.search(r"^C\n^C\n^C\n", result)
                    or "Action cancelled on user request" in error
                    or "Password len of " in error):
                return result
            log.warning('%s: Command failed: %s : RC %i' % (remote_host, command, exit_status))
            raise SshException('%s: %s' % (remote_host, error))

        log.debug('%s: Command Executed successfully: %s : RC %i' % (remote_host, command, exit_status))

        return result


class OpenSftpShell(object):

    def __init__(self, conn, debug=True):
        self._conn = conn
        self._debug = debug

    def __enter__(self):
        self._sftp = self._conn.sftp()
        return self._sftp

    def __exit__(self, type, value, traceback):
        self._sftp.close()
        self._conn.release()


class OpenShell(object):

    def __init__(self, conn, debug=True, use_channel=False):
        self._conn = conn
        self._debug = debug

    def __enter__(self):
        return self._conn.shell()

    def __exit__(self, type, value, traceback):
        self._conn.release()


class CachedSshConnection(object):

    # static varialble to hold connections that is being cached
    connections = dict()

    @staticmethod
    def shell(ip, port, username, password, ssh_key, reconnect=False):
        key = '%s-%s-%s-%s-%s-%s' % (ip, port, username, password, ssh_key, os.getpid())
        if reconnect or key not in CachedSshConnection.connections:
            CachedSshConnection.connections[key] = {
                'ssh': CachedSshConnection._connect(
                    ip, port, username, password, ssh_key),
                'time': time.time()}
        else:
            time_since_first_conn = time.time() -\
                CachedSshConnection.connections[key]['time']
            if time_since_first_conn > RemoteConstants.STDOUT_TIMEOUT / 2:
                # it is possible that the connection could have timed out by now
                # re-establish every STDOUT_TIME/2 seconds
                CachedSshConnection.connections[key] = {
                    'ssh': CachedSshConnection._connect(
                    ip, port, username, password, ssh_key),
                    'time': time.time()}
        return CachedSshConnection.connections[key]['ssh']

    @staticmethod
    def reconnect_needed(ip, port, username, password, ssh_key):
        key = '%s-%s-%s-%s-%s-%s' % (ip, port, username, password, ssh_key, os.getpid())
        if key not in CachedSshConnection.connections:
            return True
        else:
            time_since_first_conn = time.time() -\
                CachedSshConnection.connections[key]['time']
            if time_since_first_conn > RemoteConstants.STDOUT_TIMEOUT / 2:
                return True
        return False

    @staticmethod
    def _connect(ip, port, username, password, ssh_key):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        retry = 0
        while retry <= SshConnection.SSH_CONNECT_RETRY:
            log.debug('connecting to %s:%s as %s' % (ip, port, username))
            try:
                if ssh_key:
                    ssh.connect(hostname=ip, username=username, timeout=30,
                                key_filename=ssh_key)
                else:
                    ssh.connect(hostname=ip, username=username, timeout=30,
                                password=password, allow_agent=False, look_for_keys=False)
                log.debug('connection succeeded after %s attempts' % (retry + 1))
                break
            except paramiko.AuthenticationException as pax:
                log.exception(pax)
                log.error('authentication failed to ip: {ip}, please check the credentials'.format(ip=ip))
                if retry == SshConnection.SSH_CONNECT_RETRY:
                    raise SshException('paramiko.AuthenticationException to({ip})'.format(ip=ip))
            except paramiko.BadHostKeyException:
                log.error('invalid host key detected')
                if retry == SshConnection.SSH_CONNECT_RETRY:
                    raise SshException('paramiko.BadHostKeyException')
            except Exception as e:
                # FIXME : handle this if it failed due to RNG issues
                if retry == SshConnection.SSH_CONNECT_RETRY:
                    raise SshException('Error connecting to %s@%s. Unknown error: %s' % (username, ip, str(e)))
            retry = retry + 1
        return ssh


class SshConnection(object):

    SSH_CONNECT_RETRY = 10

    def __init__(self, ip, port, username, password, key, config):
        if not ip:
            raise ValueError('ip can not be null')
        if not username:
            raise ValueError('username can not be null')
        self._ip = ip
        self._port = port or 22
        self._username = username
        if not password and not key:
            raise ValueError('missing ssh_password: {password} or ssh_key: {key}. ip: {ip}'.format(password=password, key=key, ip=ip))
        self._password = password
        self._key = key
        if password and key:
            log.info('password and key are both set. will only user password')
            self._key = key
        self._connect()
        self._lock = Lock()
        self._config = config or {}

    def _connect(self, reconnect=False):
        self._ssh = CachedSshConnection.shell(self._ip, self._port, self._username,
                                              self._password, self._key, reconnect)

    def _disconnect(self):
        self._ssh.close()

    def shell(self):
        self._acquire()
        if CachedSshConnection.reconnect_needed(self._ip, self._port, self._username,
                                                self._password, self._key):
            self._connect(reconnect=True)
        transport = self._ssh.get_transport()
        if transport:
            return transport.open_session()
        else:
            # if connection is broken due to network issue and tranpsort
            # is null try to reconnect and if it is null again raise
            # an exception
            self._connect(reconnect=True)
            transport = self._ssh.get_transport()
            if not transport:
                raise SshException('%s: %s' % (self._ip, 'unable to connect'))
            return transport.open_session()

    def sftp(self):
        self._acquire()
        if CachedSshConnection.reconnect_needed(self._ip, self._port, self._username,
                                                self._password, self._key):
            self._connect()
        return self._ssh.open_sftp()

    def _acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    @property
    def ip(self):
        return self._ip

    @property
    def channel_enabled(self):
        if self._config and 'use_channel' in self._config:
            return self._config['use_channel']
        return False

    @property
    def username(self):
        return self._username


class ShellConnector(object):

    def __init__(self, ip, port, username, password, key):
        self._conn = SshConnection(ip, port, username, password, key, None)

    @classmethod
    def from_info(cls, info, user='root'):
        """
            create a shell connector from machine info object
        """
        conn = None
        if not isinstance(info, MachineInfo):
            raise TypeError('info must be a MachineInfo')
        if user == 'cmuser':
            conn = cls(info.ip, 22, info.operator_user,
                       info.operator_password, '')
        else:
            conn = cls(info.ip, 22, info.ssh_username,
                       info.ssh_password, info.ssh_key)
        return conn

    @db_retry
    def run(self, command, exit_if_error=True, log_error_as_warning=False,
            print_to_console=True):
        with OpenShell(self._conn) as os:
            return RemoteOperation.run(os, command, exit_if_error,
                                       log_error_as_warning, print_to_console)

    @db_retry
    def run_console_redirect(self, command, exit_if_error=True,
                             log_error_as_warning=False, print_to_console=True):
        """
            Alternative method 'run'. Use temporary files to save stdout &
            stderr on remote host, download it and read to output lists.
            @print_to_console: Print info messages to the console (default True)
        """

        excluded_commands = ['>', 'rm', '[ ! -d']
        # If the command already have output redirect or use 'rm' command,
        # uses major method 'run'
        for excluded_command in excluded_commands:
            if excluded_command in command:
                return self.run(command, exit_if_error, log_error_as_warning,
                                print_to_console)

        # Folder for output/error files on remote host
        rem_tmp_folder = '/tmp'
        # Prefix for output/error files
        tmp_fname_prefix = '{}'.format(str(uuid.uuid4())[0:8])
        # rco = remote command output
        tmp_out_fname = 'rco.{}.out'.format(tmp_fname_prefix)
        tmp_err_fname = 'rco.{}.err'.format(tmp_fname_prefix)
        # Remote files
        rem_tmp_out_fname = os.path.join(rem_tmp_folder, tmp_out_fname)
        rem_tmp_err_fname = os.path.join(rem_tmp_folder, tmp_err_fname)
        # Local files. Use tmp/<process id> folder on local system
        local_tmp_out_fname = '{}/{}'.format(
            TestConfigurationManager.Instance().tmp_path(),
            '{}'.format(tmp_out_fname))
        local_tmp_err_fname = '{}/{}'.format(
            TestConfigurationManager.Instance().tmp_path(),
            '{}'.format(tmp_err_fname))

        add_command = '1>{} 2>{}'.format(rem_tmp_out_fname,
                                         rem_tmp_err_fname)
        if command.endswith('|| true'):
            command = command.replace('|| true',
                                      '{} || true'.format(add_command))
        else:
            command = '{} {}'.format(command, add_command)

        self.run(command, exit_if_error, log_error_as_warning, print_to_console)
        self.download(rem_tmp_out_fname, local_tmp_out_fname, False)
        self.download(rem_tmp_err_fname, local_tmp_err_fname, False)

        self.run('rm -rf {} {}'.format(tmp_out_fname, tmp_err_fname),
                 exit_if_error, log_error_as_warning, print_to_console=False)

        result = (to_list_from_file(local_tmp_out_fname),
                  to_list_from_file(local_tmp_err_fname))
        return result

    @db_retry
    def run_interactive(self, command, input, iotimeout=0.2, iodelay=0.2):
        with OpenShell(self._conn) as os:
            return RemoteOperation.run_interactive(os, command, input, iotimeout, iodelay)

    def delete_files(self, files, force=False, recursive=True):
        # Delete all files including files inside sub-directories except the ones starting with dot
        for file in files:
            self.run("find %s -type f ! -name '.*' ! -name 'audit.log*' -exec rm -rf {} \; || true" % file)

    def stop(self, procs):
        succeeded = []
        failed = []
        self.run('killall -9 {} || true'.format(' '.join(procs)))
        return True

    def extract_as_user(self, filename, destination, as_user=None):
        if not as_user:
            raise ValueError('as_user should not be null')
        with OpenShell(self._conn) as os:
            if log.isEnabledFor(logging.DEBUG):
                RemoteOperation.run(os, 'sudo -u %s tar -xvf %s -C %s' % (as_user, filename, destination))
            else:
                RemoteOperation.run(os, 'sudo -u %s tar -xf %s -C %s' % (as_user, filename, destination))

    def extract(self, filename, destination):
        with OpenShell(self._conn) as os:
            if log.isEnabledFor(logging.DEBUG):
                RemoteOperation.run(os, 'tar -xvf %s -C %s' % (filename, destination))
            else:
                RemoteOperation.run(os, 'tar -xf %s -C %s' % (filename, destination))

    def tar(self, folders, tarfile):
        """ creates a tarball and add the specific directories and their subdirectories """
        if not folders:
            raise ValueError('folders must be set')
        if not tarfile:
            raise ValueError('tarfile must be set')
        with OpenShell(self._conn) as os:
            if log.isEnabledFor(logging.DEBUG):
                RemoteOperation.run(os, 'tar -cvf %s %s' % (tarfile, ' '.join(folders)))
            else:
                RemoteOperation.run(os, 'tar -cf %s %s' % (tarfile, ' '.join(folders)))

    def upload(self, source, destination):
        with OpenSftpShell(self._conn) as sf:
            RemoteOperation.upload(sf, source, destination)

    def download(self, source, destination, print_to_console=True):
        with OpenSftpShell(self._conn) as sf:
            RemoteOperation.download(sf, source, destination, print_to_console)

    def change_sshd_config(self, value=600):
        '''
            set the client alive interval to 30 mins
            remove the Banner
        '''
        self.run("sed -i 's/ClientAliveInterval [[:digit:]]\{{1,10\}}/ClientAliveInterval {}/g' /etc/ssh/sshd_config".format(value))
        self.run("sed -i 's/Banner \/etc\/issue.net/Banner none/g' /etc/ssh/sshd_config")
        self.run("service sshd restart")
        # FIXME: Reconnet doesn't work. (the issue with cached connection)
        # self._conn._disconnect()
        # self._conn._connect()


class ShellConnectorRaw(ShellConnector):

    """
    Version of ShellConnector that uses RemoteOperationRaw
    """

    def __init__(self, ip, port, username, password, key):
        self._conn = SshConnection(ip, port, username, password, key, None)

    def run_interactive(self, command, input, iotimeout=1.0, iodelay=1.0):
        with OpenShell(self._conn) as os:
            return RemoteOperationRaw.run_interactive(os, command, input, iotimeout, iodelay)


class ShellConnectorBash(ShellConnector):

    """
    Version of ShellConnector that uses RemoteOperationBash
    """

    def __init__(self, ip, port, username, password, key):
        self._conn = SshConnection(ip, port, username, password, key, None)

    @db_retry
    def run_interactive(self, command, input):
        with OpenShell(self._conn) as os:
            return RemoteOperationBash.run_interactive(os, command, input)

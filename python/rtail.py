import paramiko
import re
import select
import time
import threading

from cmsqalib.config import Logger

__version__ = 'v1.1'
logger = Logger.Instance().getLogger()


class LogWatchDog(object):

    """Run 'tail -f <filename>' on remote host, check with input pattern
    @substring and exit if found
    """
    # FIXME: Need add a connection watchdog (if remote server was rebooted?)

    BUFSIZE = 1024

    def __init__(self, device_info):
        self.host = device_info.ip
        self.username = device_info.ssh_username
        self.password = device_info.ssh_password
        self._stop_flag = False

    def start(self, log, substring):
        return self._worker(log, substring=substring)

    def _worker(self, log, substring, print_log=False, timeout=360):
        logger.info('Starting LogWatchDog on host [{}]...'.format(self.host))

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.host, username=self.username,
                           password=self.password)
            transport = client.get_transport()
            channel = transport.open_session()
            channel.exec_command('tail -n 1 -f {}'.format(log))
            logger.info('LogWatchDog ready to read information'
                        ' from log file [{}]'.format(log))
        except Exception as ex:
            err_msg = 'Could not start LogWatchDog for host [{}]. ' \
                      'Exception: {}'.format(self.host, ex)
            logger.error(err_msg)
            raise Exception(err_msg)

        time_start = time.time()
        line_part = ''
        while not self._stop_flag:
            if time.time() - time_start > timeout:
                self._stop_flag = True
                logger.info('LogWatchDog for log file [{}], host [{}] '
                            'has been stopped by timeout ({} sec)'
                            ''.format(log, self.host, substring, timeout))

            if channel.exit_status_ready():
                channel.close()
                channel = transport.open_session()
                channel.exec_command('tail -n 1 -f {}'.format(log))
                logger.info('LogWatchDog for log file [{}], host [{}] '
                            'has been restarted.'.format(log, self.host))

            rl, _, _ = select.select([channel], [], [], 0.0)
            if rl:
                buf = line_part + channel.recv(self.BUFSIZE)
                if buf:
                    last_eol = buf.rfind('\n')
                    if last_eol:
                        lines = buf[:last_eol]
                        line_part = buf[last_eol + 1:]
                    else:
                        lines = buf

                    for line in lines.splitlines():
                        if print_log:
                            logger.info('LogWatchDog [{}]: {}'
                                        ''.format(self.host, line))
                        if substring:
                            if re.search(substring, line):
                                self._stop_flag = True
                                logger.info('LogWatchDog [{}]: {}'
                                            ''.format(self.host, line))
                                logger.info('LogWatchDog for log file [{}], '
                                            'host [{}] found substring [{}] '
                                            'and has been stopped ({} sec)'
                                            ''.format(log, self.host,
                                                      substring,
                                                      time.time() - time_start))
                                sleep = 30
                                logger.info("Sleeping {} sec more after finding the"
                                            " substring {}".format(sleep, substring))
                                time.sleep(sleep)

        channel.close()
        transport.close()
        client.close()


def _rtail_worker(devices, log, statement):
    if not isinstance(devices, list):
        devices = [devices]

    th_log = list()
    for device in devices:
        th_log.append(threading.Thread(target=LogWatchDog(device).start,
                                       args=(log, statement,)))
    map(lambda x: x.start(), th_log)
    map(lambda x: x.join(), th_log)


def rtail_broker_orchestrator(devices):
    return _rtail_worker(devices,
                         '/opt/cri/cm/log/orchestrator/orchestrator.log',
                         'Done with Broker app now')

def rtail_broker_scheduler(devices):
    return _rtail_worker(devices,
                         '/opt/cri/cm/log/scheduler/scheduler-main.log',
                         'Done with Broker Scheduler startup')

def rtail_broker_event(devices):
    return _rtail_worker(devices,
                         '/opt/cri/cm/log/event/event.log',
                         'Done with Event Microservice startup')
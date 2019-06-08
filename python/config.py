import ConfigParser
import logging.config
import uuid
import shutil

import os
import re
import subprocess

from cmsqalib import testconfig
from cmsqalib.geolocconstants import GeoLocConstants, SfoGeoLocConstants, IdcGeoLocConstants
from cmsqalib.util.misc import get_module_pardir


class GlobalSingleton:

    """ a non thread-safe helper class to implement singletons.
        This should be used as a decorator to the class that
        should be a singleton
        The decorated class need to define an __init__ function
        that takes self argument.

        Limitation: the singleton decorated class can not be inherited
        from

        based on a response in :
        http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
    """

    def __init__(self, decorated):
        self._decorated = decorated
        self._pid = os.getpid()

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed via Instance() method')

    def __instance_check__(self, inst):
        return isinstance(inst, self._decorated)


class Singleton:

    """ a non thread-safe helper class to implement singletons.
        This should be used as a decorator to the class that
        should be a singleton
        The decorated class need to define an __init__ function
        that takes self argument.

        Limitation: the singleton decorated class can not be inherited
        from

        based on a response in :
        http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
    """

    def __init__(self, decorated):
        self._decorated = decorated
        self._pid = os.getpid()

    def Instance(self):
        # if the current process is different than the original one then
        # we need to re-create this singleton
        if int(os.getpid()) != int(self._pid):
            self._pid = os.getpid()
            self._instance = self._decorated()
            return self._instance
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed via Instance() method')

    def __instance_check__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class TestConfigurationManager(object):

    def __init__(self):
        # instead of using the time it is better to use the PID
        self._uuid = "{}-{}".format(str(os.getpid()), str(uuid.uuid4())[0:4])
        self._tmp_dir = None
        self._save_compare_dir = None
        self._log_dir = None
        self._cmsim_dir = None
        self._root_artifacts_dir = None

    def logs_path(self):
        if self._log_dir is None:
            self.set_tmp_path('tmp', True)
        return self._log_dir

    def force_path_existence(self, base_dir, sub_dir=''):
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        if sub_dir:
            if not os.path.isdir(sub_dir):
                os.mkdir(sub_dir)

    def set_tmp_path(self, new_path, uuid_subdir=True):
        self._log_dir = new_path
        self._tmp_dir = new_path
        if (uuid_subdir):
            self._tmp_dir += '/%s' % self._uuid
            self.force_path_existence(self._log_dir, self._tmp_dir)
        else:
            self.force_path_existence(self._log_dir)

    def tmp_path(self):
        if self._tmp_dir is None:
            self.set_tmp_path('tmp', True)
        return self._tmp_dir

    def save_compare_path(self):
        if self._save_compare_dir is None:
            self.set_save_compare_path('compare')
        return self._save_compare_dir

    def set_save_compare_path(self, new_path, uuid_subdir=False):
        self._save_compare_dir = '%s/' % new_path
        self.force_path_existence(self._save_compare_dir)

    @property
    def uuid(self):
        return self._uuid

    def new_temp_filename(self, name=None):
        if not name:
            name = '{}.tmp'.format(self._uuid)
        return '{}/{}'.format(TestConfigurationManager.Instance().tmp_path(), name)

    @property
    def resources_path(self):
        return os.path.join(get_module_pardir(__file__), 'resources')

    @property
    def dependencies_path(self):
        return os.path.join(os.getcwd(), 'dependencies')

    @property
    def dependencies_template_path(self):
        return os.path.join(self.dependencies_path, 'templates')

    @property
    def dependencies_receipients_path(self):
        return os.path.join(self.dependencies_path, 'receipients')

    @property
    def dependencies_lib_path(self):
        return os.path.join(self.dependencies_path, 'lib')

    def results_path(self):
        return self.logs_path()

    def cmsim_path(self, perm_subdir=None):

        if perm_subdir:
            self._cmsim_dir = PermCmSimManager.Instance().cmsim_path(perm_subdir)

        if not self._cmsim_dir:
            self._cmsim_base_dir = TestConfigurationManager.Instance().tmp_path()
            self._cmsim_dir = "{}/{}".format(self._cmsim_base_dir, 'cmsim')
            self.force_path_existence(self._cmsim_dir)
        return self._cmsim_dir

    def root_artifacts_path(self, perm_subdir=None):

        if not self._root_artifacts_dir:
            self.cmsim_path(perm_subdir)
            self._root_artifacts_dir = '/'.join((self._cmsim_dir, 'root_dataset',))
            self.force_path_existence(self._root_artifacts_dir)
        return self._root_artifacts_dir


@GlobalSingleton
class PermCmSimManager(object):

    def __init__(self):
        self._uuid = "{}-{}".format(str(os.getpid()), str(uuid.uuid4())[0:4])
        self._datastore_base_dir = os.path.join(get_module_pardir(__file__), 'datastore')
        self._datastore_dir = None
        self._cmsim_dir = None
        self._tmp_dir = None

    def set_tmp_path(self, new_path):
        self._tmp_dir = new_path
        self.force_path_existence(self._tmp_dir)

    def tmp_path(self):
        if self._tmp_dir is None:
            new_path = '/'.join(('tmp', self._uuid))
            self.set_tmp_path(new_path)
        return self._tmp_dir

    def force_path_existence(self, base_dir, sub_dir=''):
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        if sub_dir:
            if not os.path.isdir(sub_dir):
                os.mkdir(sub_dir)

    def _set_datastore_dir(self, subdir):
        self._datastore_dir = "{}/{}".format(self._datastore_base_dir, subdir)

    def _set_cmsim_dir(self, subdir):
        self._set_datastore_dir(subdir)
        self._cmsim_dir = "{}/{}".format(self._datastore_dir, 'cmsim')

    def datastore_path(self, subdir):
        if self._datastore_dir is None:
            self._set_datastore_dir(subdir)
            self.force_path_existence(self._datastore_dir)
        return self._datastore_dir

    def cmsim_path(self, subdir):
        if self._cmsim_dir is None:
            self._set_cmsim_dir(subdir)
            self.force_path_existence(self._cmsim_dir)
        return self._cmsim_dir

    def clean_perm_cmsim(self, subdir):
        dir = "{}/{}/{}".format(self._datastore_base_dir, subdir, 'cmsim')
        shutil.rmtree(dir)


class ClassLoggingAdapter(logging.LoggerAdapter):

    """
    Add the class name to a log message
    """

    def process(self, msg, kwargs):

        # Crazy debug stuff
        # print vars (self)
        # print self.logger.name
        # print vars(self.logger)
        # print msg
        # print kwargs

        # More sane, but not as effective means to log the classname
        return '[%s] %s' % (self.extra['className'], msg), kwargs

        # Override the 'name' attribute and return to the message
        #self.logger.name = self.extra['className']
        # return '%s' % msg, kwargs


@Singleton
class LogConfigFileName:

    TEMPLATE_NAME = 'logging.conf.sample'

    def __init__(self):
        log_path = TestConfigurationManager.Instance().logs_path()
        # check if the path exists otherwise try and create it
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        # choosing .txt to be mroe friendly to CI server
        name = ''.join(['log-proc-', str(os.getpid()), '.txt'])
        self._config_file = ''.join([log_path, '/', str(os.getpid()), '-logging.conf'])
        log_file = ''.join([log_path, '/', name])
        self._create_log_config(self._config_file, log_file, 'INFO')

    def get_config_file(self):
        return self._config_file

    def get_template_fname(self):
        return os.path.join(get_module_pardir(__file__), self.TEMPLATE_NAME)

    def _create_log_config(self, config_filename, log_filename, level):
        template_fname = self.get_template_fname()
        template = open(template_fname)
        config = open(config_filename, 'w')
        config.truncate()
        for line in template:
            config.write(line.replace('@@LEVEL@@', level)
                         .replace('@@FILENAME@@', log_filename))
        config.close()
        template.close()


@Singleton
class Logger:

    def __init__(self):
        self._new_logger()

    def _new_logger(self):
        logging.config.fileConfig(LogConfigFileName.Instance().get_config_file(),
                                  disable_existing_loggers=False)
        self._logger = logging.getLogger()

    def getLogger(self):
        return self._logger


@GlobalSingleton
class GeoLocManager(object):

    """
    Singleton manager object for Geo Location.
    """

    def __init__(self):
        self._geoloc = None
        self._constants = None

    def _set_geoloc_constants(self):
        if self._geoloc == 'sfo':
            self._constants = SfoGeoLocConstants()
        elif self._geoloc == 'idc':
            self._constants = IdcGeoLocConstants()
        else:
            self._constants = GeoLocConstants()

    def _get_geoloc(self):
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '..', 'conf/GEOLOC'
        )
        with open(file_path, 'rb') as f:
            self._geoloc = f.readline().strip()

    def _set_geoloc(self):
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '..', 'conf/GEOLOC'
        )
        with open(file_path, 'rb') as f:
            self._geoloc = f.readline().strip()

        self._set_geoloc_constants()

    @property
    def constants(self):
        if not self._constants:
            self._set_geoloc()
        return self._constants

    @property
    def geoloc(self):
        if not self._geoloc:
            self._get_geoloc()
        return self._geoloc


class Branch(object):

    @staticmethod
    def get_name_from_version_file(file_path=None):
        branch_name = None

        file_path = file_path or \
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                         'VERSION')

        with open(file_path, 'rb') as f:
            branch_name = f.readline().strip()

        return branch_name

    @staticmethod
    def get_name_from_git_branch(git_folder=None):
        branch_name = None
        re_branch_name = '(-> origin\/)(.+)'

        orig_working_dir = os.getcwd()
        os.chdir(git_folder or os.path.dirname(os.path.realpath(__file__)))
        output = subprocess.Popen(["git", "branch", "-r"],
                                  stdout=subprocess.PIPE).communicate()[0]
        os.chdir(orig_working_dir)

        for line in output.split('\n'):
            result = re.findall(re_branch_name, line)
            if result:
                branch_name = result[0][1]
                break

        return branch_name


class MachineInfo(object):

    ip = ''
    ssh_port = 22
    ssh_username = 'root'
    ssh_password = 'cryptomanager'
    ssh_key = ''
    startup_env_vars = list()
    operator_user = ''
    operator_password = ''
    cmdevice = 'notactivated'
    hsm = 'hsmsim'      # WARNING DEPRECATED
    hsm_location = '4002@localhost'
    deviceid = ''
    alias = ''

    def __repr__(self):
        return '{}:ip:{}'.format(self.__class__.__name__, self.ip)


class ServiceInfo(MachineInfo):
    admin = ''
    password = ''
    installation_path = ''
    web_service_port = 443
    web_protocol = 'https'
    ui_port = 80
    ui_username = ''
    ui_password = ''
    db_type = 'oracle'
    hsm = 'hsmsim'                          # WARNING DEPRECATED
    hsm_location = '4002@localhost'
    nfs_mount = ''
    properties = ''
    device_type = 'SERVICE'
    device_image = 'cmservice'


class SoftRaInfo(MachineInfo):
    installation_path = ''


class CrispInfo(MachineInfo):
    installation_path = ''
    hsm = 'hsmsim'                              # WARNING DEPRECATED
    hsm_location = '4002@localhost'
    device_image = 'crisp'


class ApplianceClusterInfo(object):
    appliancecluster_id = None
    appliances = list()
    branch = None
    buildnum = None


class ServiceClusterInfo(object):
    servicecluster_id = None
    appliance_clusters = list()
    services = list()
    job_interval = ''
    db_prefix = None
    db_host = None
    db_user = None
    db_password = None


class ApplianceInfo(MachineInfo):
    admin = ''
    password = ''
    installation_path = ''
    hsm = 'hsmsim'                                 # WARNING DEPRECATED
    vmname = ''
    hsm_location = '4002@localhost'
    trr0_prod = False
    appliance_id = ''
    cluster_id = ''
    device_type = 'APPLIANCE'
    device_image = 'appliance'


class RootArtifactsInfo(object):
    base_dir = ''
    dataset = ''


class RootInfo(MachineInfo):
    admin = ''
    password = ''
    installation_path = ''
    hsm = 'hsmsim'                                      # WARNING DEPRECATED
    hsm_location = '4002@localhost'
    device_type = 'ROOT'
    device_image = 'root'
    instancename = 'Commercial'


class RootCAInfo(MachineInfo):

    def __init__(self):
        super(RootCAInfo, self).__init__()


class ConfigItems:

    appliances = list()
    service = list()
    clusters = set()
    roots = list()
    softras = list()
    crisps = list()
    branch = {}
    rootca = None
    root_artifacts = None
    cmclient_so = ''
    cmsim_cfg = None
    params = {}
    service_clusters = dict()
    appliance_clusters = dict()
    restore_box = list()
    ui = False

    def __init__(self, ini):
        self._config = ConfigParser.ConfigParser()
        self._config.read(ini)
        self.params = testconfig.config
        if 'nosetests.config' in self.params:
            self.params.update(self.params['nosetests.config'])
        self._populate(self._config)

    def get(self, section, option):
        """
            this function is only used by wildcats-usecases.py test case
            do not use this function for CM tests
        """
        return self._config.get(section, option)

    def _list_ids(self, config, section):
        ids = []
        options = config.options(section)
        for option in options:
            ids.append(config.get(section, option))
        return ids

    def _extract_kvs(self, comma_sep_kvs):
        if comma_sep_kvs:
            return comma_sep_kvs.split(',')
        else:
            return list()

    def _populate(self, config):
        self.services = []
        self.appliances = []
        self.clusters = set()
        self.root_artifacts = {}
        self.appliance_cluster_id_obj_map = dict()
        self.appliance_clusters = dict()
        self.applianceclusterid_applianceinfo_map = dict()
        self.serviceclusterid_servicedeviceinfo_map = dict()
        self.restore_box = []
        self.ui = False
        self.branch = {}
        self.mysql = dict()
        appliance_cluster_objs = list()
        service_cluster_objs = list()

        if config.has_section('appliances'):
            app_ids = self._list_ids(config, 'appliances')
            self.appliances = [self._convert_to_attribute(config, ApplianceInfo(), app_id) for app_id in app_ids]
        if config.has_section('root'):
            if len(self._list_ids(config, 'root')) > 0:
                root_ids = self._list_ids(config, 'root')
                self.roots = [self._convert_to_attribute(config, RootInfo(), root_id) for root_id in root_ids]
        if config.has_section('softra'):
            if len(self._list_ids(config, 'softra')) > 0:
                softra_ids = self._list_ids(config, 'softra')
                self.softras = [self._convert_to_attribute(config, SoftRaInfo(), softra_id) for softra_id in softra_ids]
        if config.has_section('services'):
            if len(self._list_ids(config, 'services')) > 0:
                service_ids = self._list_ids(config, 'services')
                self.services = [self._convert_to_attribute(config, ServiceInfo(), service_id) for service_id in service_ids]
        if config.has_section('crisp'):
            if len(self._list_ids(config, 'crisp')) > 0:
                crisp_ids = self._list_ids(config, 'crisp')
                self.crisps = [self._convert_to_attribute(config, CrispInfo(), crisp_id) for crisp_id in crisp_ids]
        if config.has_section('applianceclusters'):
            if len(self._list_ids(config, 'applianceclusters')) > 0:
                appliance_cluster_ids = self._list_ids(config, 'applianceclusters')
                appliance_cluster_objs = [self._convert_to_attribute(config, ApplianceClusterInfo(), appliance_cluster_id)
                                          for appliance_cluster_id in appliance_cluster_ids]
        if config.has_section('serviceclusters'):
            if len(self._list_ids(config, 'serviceclusters')) > 0:
                service_cluster_ids = self._list_ids(config, 'serviceclusters')
                service_cluster_objs = [self._convert_to_attribute(config, ServiceClusterInfo(), service_cluster_id)
                                        for service_cluster_id in service_cluster_ids]

        self.cmclient_so = ''
        self.cmta_so = ''

        if config.has_section('cmclient') and config.has_option('cmclient', 'cmclient-so'):
            self.cmclient_so = config.get('cmclient', 'cmclient-so')

        if config.has_section('cmclient') and config.has_option('cmclient', 'cmta-so'):
            self.cmta_so = config.get('cmclient', 'cmta-so')

        if config.has_section('cmsim') and config.has_option('cmsim', 'cmsim-cfg'):
            self.cmsim_cfg = config.get('cmsim', 'cmsim-cfg')

        if config.has_section('modules'):
            modules = dict(config.items('modules'))
            self.params.update(
                dict(map(lambda (key, value): ("modules.%s" % key, value), modules.items())))

        if config.has_section('root-artifacts'):
            self.root_artifacts = dict(config.items('root-artifacts'))

        if config.has_section('restore_box'):
            if len(self._list_ids(config, 'restore_box')) > 0:
                restore_box_ids = self._list_ids(config, 'restore_box')
                self.restore_box = [self._convert_to_attribute(config, RootInfo(),
                                                               restore_box_id) for restore_box_id in restore_box_ids]

        if config.has_section('branch'):
            self.branch = {'release': config.get('branch', 'release'),
                           'feature': config.get('branch', 'feature')}

        applianceclusterid_applianceinfo_map = dict()

        for appliance in self.appliances:
            if appliance.cluster_id in self.applianceclusterid_applianceinfo_map:
                self.applianceclusterid_applianceinfo_map[appliance.cluster_id].append(appliance)
            else:
                self.applianceclusterid_applianceinfo_map[appliance.cluster_id] = [appliance]

        applianceclusterid_applianceclusterinfo_map = dict()
        for appliance_cluster_obj in appliance_cluster_objs:
            if appliance_cluster_obj.appliancecluster_id in self.applianceclusterid_applianceinfo_map:
                applianceclusterid_applianceclusterinfo_map[appliance_cluster_obj.appliancecluster_id] = appliance_cluster_obj
                appliance_cluster_obj.appliances = self.applianceclusterid_applianceinfo_map[appliance_cluster_obj.appliancecluster_id]
                if appliance_cluster_obj.appliancecluster_id in self.appliance_clusters:
                    self.appliance_clusters[appliance_cluster_obj.appliancecluster_id].append(appliance_cluster_obj)
                else:
                    self.appliance_clusters[appliance_cluster_obj.appliancecluster_id] = appliance_cluster_obj

        self.clusters = [appliance_cluster_obj for appliance_cluster_obj in appliance_cluster_objs]
        for service in self.services:
            if service.service_id not in self.serviceclusterid_servicedeviceinfo_map:
                self.serviceclusterid_servicedeviceinfo_map[service.service_id] = [service]
            else:
                self.serviceclusterid_servicedeviceinfo_map[service.service_id].append(service)

        for service_cluster_obj in service_cluster_objs:
            if service_cluster_obj.servicecluster_id in self.serviceclusterid_servicedeviceinfo_map:
                service_cluster_obj.services = self.serviceclusterid_servicedeviceinfo_map[service_cluster_obj.servicecluster_id]
                service_cluster_obj.appliance_clusters = list()
                if hasattr(service_cluster_obj, 'appliancecluster_ids'):
                    appliancecluster_ids = service_cluster_obj.appliancecluster_ids.strip().split(',')
                    for appliancecluster_id in appliancecluster_ids:
                        if appliancecluster_id in applianceclusterid_applianceclusterinfo_map:
                            appliancecluster_obj = applianceclusterid_applianceclusterinfo_map[appliancecluster_id]
                            service_cluster_obj.appliance_clusters.append(appliancecluster_obj)
                self.service_clusters[service_cluster_obj.servicecluster_id] = service_cluster_obj
        devices = self.roots + self.appliances + self.services + self.crisps
        for device in devices:
            if not device.alias:
                device.alias = device.ip
        # initialize rootca
        rootca = RootCAInfo()
        rootca.ssh_username = 'root'
        rootca.ssh_password = 'cryptomanager'
        rootca.ip = 'sfxsv-cm-rootca'
        self.rootca = rootca

    def get_cluster_info(self, appliance):
        cluster_id = appliance.cluster_id
        return self.appliance_clusters[cluster_id]

    def _convert_to_attribute(self, config, obj, name):
        for option in config.options(name):
            setattr(obj, option, config.get(name, option))
        return obj

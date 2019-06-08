import argparse
import ssl
import os
import sys

from cmsqalib.bat import BATTest
from cmsqalib.config import ConfigItems, Branch, Logger
from cmsqalib.deploy import Deploy, CmServiceSetup
from cmsqalib.provision import Provision
from cmsqalib.provision.devices import HwDevice
from cmsqalib.util.es_kafka_config import EsAndKafkaConfig
from cmsqalib.util.verify_services import VerifyServices
from cmsqalib.util.production_sanity import ProductionSanity
from cmsqalib.util.clear_bond0 import ClearBond0
from cmsqalib.util.mock import record, replay, kafka_record, kafka_replay
from cmsqalib.util.multiproccessutil import CtrlCSignalHandler
from cmsqalib.util.nginx_config import NginxConfig
from cmsqalib.util.vpn import VpnTools
from cmsqalib.criplatform.criosutil import CRIOSUtil

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

logger = Logger.Instance().getLogger()

__version__ = '0.3.0'

ACTDEF_MOCK_STATE = 'actdef'
INV_MOCK_STATE = 'inventory'
KAFKA_MOCK_STATE = 'kafka'


def args_parser():
    """ Parse commnand line arguments """

    parser = argparse.ArgumentParser(description='CM test infrastructure configuration tool.')
    parser.add_argument('--config', default='config.ini',
                        help='config file to read params from')

    parser.add_argument('--provision', action='store_true', default=False,
                        help='Provision HW & VM devices based on CONFIG')
    parser.add_argument('--provision-hw-script-copy', action='store_true',
                        default=False,
                        help='Always copy provision script to HW device')
    parser.add_argument('--provision-hw-script-path', default=None,
                        help='Local path to provision script')
    parser.add_argument('--sequential-provision', action='store_true',
                        default=False,
                        help='Doing sequential provision')
    parser.add_argument('--install', action='store_true', default=False,
                        help='install RPMs in parallel')
    parser.add_argument('--setup-vpn', action='store_true', default=False, dest='setup_vpn',
                        help='Setup VPN between Service & Appliance hosts')
    parser.add_argument('--cleanup-vpn', action='store_true', default=False, dest='cleanup_vpn',
                        help='Cleanup VPN settings between Service & Appliance'
                        ' hosts')
    parser.add_argument('--cleanup-vpn-map', default=None, dest='cleanup_vpn_map',
                        help='Cleanup VPN settings between hosts from '
                        '"hosts.map" file. Input: host name with file '
                        '"hosts.map"')

    parser.add_argument('--branch', help='jenkins release branch to provision',
                        default=None)
    parser.add_argument('--build', default='latestbuilds',
                        help='jenkins build number to provision')
    parser.add_argument('--geolocation', default='sfo', choices=('sfo', 'idc'),
                        help='geolocation to provision')
    parser.add_argument('--image-path', default=None,
                        help='path to local user folder with images, '
                             'for a developer this is typically ../install/images')

    parser.add_argument('--bat', action='store_true', default=False,
                        help='BAT test')
    # mock record and replay parameters
    parser.add_argument('--record', nargs='+',
                        help='create mock objects: actdef|inventory|kafka|all')
    parser.add_argument('--replay', nargs='+',
                        help='replay mock objects: actdef|inventory|kafka|all')
    parser.add_argument('--artifacts', default='/tmp/mock',
                        help='mock objects parent folder')

    parser.add_argument('--geoloc', dest='geoloc', default='sfo',
                        help='geolocations to deploy. By default, deploy.py \n'
                             + 'will install the sfo location.\n')
    parser.add_argument('--rbmap', dest='rbmap', default='',
                        help='Release to build number map\n'
                             + 'Example: --rbmap 1.1.0:311,1.2.0:30')
    parser.add_argument('--onlysetup', action='store_true',
                        help='Only setup steps, without rpms installation')
    parser.add_argument('--prodkey', action='store_true',
                        help='Use the prod keys for the firmware')
    parser.add_argument('--onlyrpm', action='store_true',
                        help='Only rpms installation, without setup steps')
    parser.add_argument('--nginx', action='store_true', default=False,
                        help='Appliance Nginx configure')
    parser.add_argument('--service', action='store_true', default=False,
                        help='Service setup')
    parser.add_argument('--mirrormaker', action='store_true', default=False,
                        help='Service MirrorMaker setup')
    parser.add_argument('--kafka', action='store_true', default=False,
                        help='Appliance Kafka setup')
    parser.add_argument('--verify_microservices', action='store_true', default=False,
                        help='Verify Micro Services')
    parser.add_argument('--disable_fluentd', action='store_true', default=False,
                        help='Disable Fluentd Service on CM Service and CM Appliance')
    parser.add_argument('--upgrade-testing', action='store_true', default=False,
                        dest='upgrade_testing',
                        help='For configuring setup for upgrade testing')
    parser.add_argument('--clear-hsm', action='store_true', default=False,
                        help='Clear the mdlsigalt.key and cm.msc from Flash')
    parser.add_argument('--production-sanity', default='qualcomm', choices=('qualcomm', 'micron'),
                        help='Production Sanity Validation')
    parser.add_argument('--clear-bond0', action='store_true', default=False,
                        help='Clear the Bond0 interface')

    args = parser.parse_args()
    args.record_actdef = False
    args.record_inv = False
    args.record_kafka = False
    args.record_all = False
    args.replay_all = False
    args.replay_actdef = False
    args.replay_inv = False
    args.replay_kafka = False
    args.actdef_mock_state = ACTDEF_MOCK_STATE
    args.inv_mock_state = INV_MOCK_STATE
    args.kafka_mock_state = KAFKA_MOCK_STATE
    if args.record:
        if ACTDEF_MOCK_STATE in args.record:
            args.record_actdef = True
        if INV_MOCK_STATE in args.record:
            args.record_inv = True
        if KAFKA_MOCK_STATE in args.record:
            args.record_kafka = True
        if 'all' in args.record:
            args.record_all = True
    if args.replay:
        if ACTDEF_MOCK_STATE in args.replay:
            args.replay_actdef = True
        if INV_MOCK_STATE in args.replay:
            args.replay_inv = True
        if KAFKA_MOCK_STATE in args.replay:
            args.replay_kafka = True
        if 'all' in args.replay:
            args.replay_all = True

    if args.image_path:
        if 'http' not in args.image_path:
            # If --image-path was specified, make sure that we
            # convert it an absolute path so that any subsequent
            # cd operations will still allow it to be accessed
            # correctly.
            args.image_path = os.path.abspath(args.image_path)
    return args


def print_args(args):
    out_line_format = '{:<14}{}'
    logger.info(out_line_format.format('CONFIG', args.config))
    logger.info(out_line_format.format('BRANCH', args.branch))
    logger.info(out_line_format.format('BUILD', args.build))
    logger.info(out_line_format.format('GEOLOCATION', args.geolocation))
    logger.info(out_line_format.format('IMAGE PATH', args.image_path))


def exit_code(res, action_name):
    if res:
        logger.info('The action "{}" has been completed.'
                    ''.format(action_name))
    else:
        logger.error('The action "{}" has not been completed.'
                     ''.format(action_name))
        sys.exit(-1)


def main():
    args = args_parser()
    config = ConfigItems(args.config)
    args.branch = args.branch or config.branch['feature']
    print_args(args)
    result = True

    # Provision task
    if args.provision:
        if args.provision_hw_script_copy:
            HwDevice.COPY_PROVISION_SCRIPT = True
        if args.provision_hw_script_path:
            HwDevice.IMAGE_PROVISION_SCRIPT_SOURCE = \
                args.provision_hw_script_path
        p = Provision(config, args.branch, args.build, args.image_path,
                      args.geolocation, args.upgrade_testing, args.sequential_provision)
        exit_code(p.run(), 'Provision')

    # rpminstall task
    elif args.install:
        args.cm = args.build
        args.cmroot = args.build
        args.cmcrisp = args.build
        args.cmapp = args.build
        args.cmserv = args.build
        args.release_branch = args.branch
        args.params = ''
        deploy = Deploy(args)
        procs = list()
        CtrlCSignalHandler(procs)
        deploy.install_parallel(procs)

    # VPN setup task
    elif args.setup_vpn:
        vpn = VpnTools(config)
        exit_code(vpn.setup(), 'VPN setup')
        exit_code(vpn.add_hosts(), 'Add hosts to VPN mesh')

    # VPN cleanup task (based on config)
    elif args.cleanup_vpn:
        vpn = VpnTools(config)
        exit_code(vpn.cleanup(), 'VPN cleanup ({})'.format(args.config))

    # VPN cleanup task (based on hosts.map)
    elif args.cleanup_vpn_map:
        vpn = VpnTools(config)
        exit_code(vpn.cleanup_hosts_map(args.cleanup_vpn_map),
                  'VPN cleanup (hosts.map)')

    # BAT test
    elif args.bat:
        bat = BATTest(args)
        bat.SEQUENTIAL = True
        exit_code(bat.run(), 'BAT test')

    #  Replay activation/definition mock objects
    elif args.replay_actdef:
        try:
            replay(os.path.join(args.artifacts, ACTDEF_MOCK_STATE), config)
            NginxConfig.cmappliance(config.appliance_clusters)
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Replay activation/definition mock objects')

    #  Replay inventory mock objects
    elif args.replay_inv:
        try:
            replay(os.path.join(args.artifacts, INV_MOCK_STATE), config)
            NginxConfig.cmappliance(config.appliance_clusters)
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Replay inventory mock objects')

    # Replay appliance kafka configuration
    elif args.replay_kafka:
        exit_code(kafka_replay(os.path.join(args.artifacts, KAFKA_MOCK_STATE), config),
                  'Replay appliance kafka configuration mock objects')

    #  Record activation/definition mock objects
    elif args.record_actdef:
        try:
            record(os.path.join(args.artifacts, ACTDEF_MOCK_STATE), config)
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Record activation/definition mock objects')

    #  Record inventory mock objects
    elif args.record_inv:
        try:
            record(os.path.join(args.artifacts, INV_MOCK_STATE), config)
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Record inventory mock objects')

    # Record appliance kafka configuration
    elif args.record_kafka:
        exit_code(kafka_record(os.path.join(args.artifacts, KAFKA_MOCK_STATE), config),
                  'Record appliance kafka configuration mock objects')

    # setup nginx
    elif args.nginx:
        try:
            NginxConfig.cmappliance(config.appliance_clusters)
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Appliance Nginx setup')

    # cmservice setup
    elif args.service:
        try:
            service_setup = CmServiceSetup(config.services, config.service_clusters)
            service_setup.setup()
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'CM Service setup')

    # cmservice mirror maker
    elif args.mirrormaker:
        try:
            service_setup = CmServiceSetup(config.services, config.service_clusters)
            service_setup.mirror_maker()
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Service MirrorMaker setup')

    # appliance kafka setup
    elif args.kafka:
        try:
            EsAndKafkaConfig.provisioner(config.appliance_clusters)
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Appliance Kafka setup')

    elif args.verify_microservices:
        try:
            verify_services = VerifyServices()
            verify_services.verify_microservices()
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Verify Micro Services')

    elif args.disable_fluentd:
        try:
            devices = config.services + config.appliances
            CRIOSUtil.disable_fluentd(devices)
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Disable Fluentd Service')

    elif args.clear_hsm:
        try:
            sanity = ProductionSanity(args.production_sanity)
            sanity.clear_hsm()
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Clear mdlsigalt.key and cm.msc')

    elif args.production_sanity:
        try:
            sanity = ProductionSanity(args.production_sanity)
            sanity.production_sanity()
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Production Sanity Validation')

    elif args.clear_bond0:
        try:
            clear_bond0 = ClearBond0()
            clear_bond0.clear_bond0_interface()
        except Exception as e:
            logger.exception(e)
            result = False
        exit_code(result, 'Clear Bond0 Interface')
    else:
        logger.info('Nothing to do')


if __name__ == '__main__':
    main()

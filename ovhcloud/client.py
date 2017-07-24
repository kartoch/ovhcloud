import argparse
import logging
import sys

import ovh

from ovhcloud.api_cache import ApiCacheCommand
from ovhcloud.version import VersionCommand


class OVHClient(object):

    _action_cls = [VersionCommand, ApiCacheCommand]

    def __init__(self, args, ovh_client=None):
        self._actions = {cls.name: cls(self) for cls in self._action_cls}
        self._parse_arguments(args)
        for action in self._actions.values():
            action.set_logging()
        self._ovh_client = ovh.Client() if ovh_client is None else ovh_client

    def _parse_arguments(self, args):
        parser = argparse.ArgumentParser(prog='ovhcloud')
        log_group = parser.add_mutually_exclusive_group()
        log_group.add_argument(
            '-d', '--debug',
            help="Print lots of debugging statements",
            action="store_const", dest="log_level", const=logging.DEBUG,
            default=logging.WARNING,
        )
        log_group.add_argument(
            '-v', '--verbose',
            help="Be verbose",
            action="store_const", dest="log_level", const=logging.INFO,
        )
        log_group.add_argument("-l", "--log", dest="log_level",
                               choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                               help="Set the logging level")
        subparsers = parser.add_subparsers(dest="group_or_command")
        for k in self._actions.keys():
            subparser = subparsers.add_parser(k)
            self._actions[k].parser(subparser)

        self._args = parser.parse_args(args)

        try:
            logging.basicConfig(level=getattr(self._args, 'log_level'))
        except AttributeError:
            logging.basicConfig(level='WARNING')
        self.log = logging.getLogger(__name__)

    def action(self):
        command_cls_action = self._actions.get(self._args.group_or_command)
        command_cls_action.action()


def main():
    client = OVHClient(sys.argv[1:])
    client.action()


if __name__ == '__main__':
    main()

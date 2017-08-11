import logging
import sys

import ovhcloud
from ovhcloud.cache import ApiCacheCommand
from ovhcloud.generate_args import GenerateArguments


class OVHClient(object):

    _action_cls = {
        'cache': ApiCacheCommand
    }

    def __init__(self, args, _configuration_dir=None):
        self.configuration_dir = ovhcloud.DEFAULT_CONFIGURATION_DIR if _configuration_dir is None else _configuration_dir
        self._actions = {name: cls(self) for name, cls in self._action_cls.items()}
        self._parse_arguments(args)
        for action in self._actions.values():
            action.set_logging()

    @property
    def configuration_dir(self):
        return self._configuration_dir

    @configuration_dir.setter
    def configuration_dir(self, value):
        self._configuration_dir = value
        self._cache_file = ovhcloud.DEFAULT_ENDPOINTS_API_CACHE

    @property
    def cache_file(self):
        return self._cache_file

    def _parse_arguments(self, args: str):
        p = GenerateArguments(self)
        p.build_parser(self._actions)
        p.analyze_args(args)
        self._args = p.args
        self._log = logging.getLogger(__name__)

    def action(self):
        command_cls_action = self._actions.get(self._args.group_or_command)
        command_cls_action.action()


def main():
    client = OVHClient(sys.argv[1:])
    client.action()


if __name__ == '__main__':
    main()

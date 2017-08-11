import json
import logging
import sys
from argparse import ArgumentParser

import ovh
from ovh import Client

import ovhcloud


class GenerateArguments(object):
    def __init__(self, client: Client):
        self._parser = ArgumentParser(prog='ovhcloud')
        self._client = client
        self._path_arguments = _FixedPathArgument('/')

    def build_parser(self, actions):
        self._parse_flags()
        subparsers = self._parser.add_subparsers(dest="group_or_command")
        self._parse_commands(subparsers, actions)
        self._parse_api(subparsers)

    def analyze_args(self, args):
        self._args = self._parser.parse_args(args)
        logging.basicConfig(level=getattr(self.args, 'log_level'))
        if self.args.group_or_command is None:
            self._parser.print_help()
            sys.exit(1)

    @property
    def args(self):
        return self._args

    def _parse_flags(self):

        # parse log flags
        self._parser.add_argument(
            '-d', '--debug',
            help="Print lots of debugging statements",
            action="store_const",
            dest="log_level",
            const=logging.DEBUG,
            default=logging.WARNING
        )

        # parse endpoint flag
        self._parser.add_argument(
            '-e', '--endpoint',
            help="Select the endpoint",
            choices=ovh.client.ENDPOINTS.keys(),
            dest="endpoint",
            default="ovh-eu"
        )

        # parse version flag
        self._parser.add_argument('-v', '--version', action='version', version=ovhcloud.__version__)

    def _parse_commands(self, subparsers: ArgumentParser, actions: dict):
        for k in actions.keys():
            subparser = subparsers.add_parser(k)
            actions[k].parser(subparser)

    def _parse_api(self, subparsers: ArgumentParser):
        f = open(self._client.cache_file)
        c: dict = json.load(f)

        for endpoint in c.items():
            for root_path in endpoint[1]["paths"].items():
                if root_path[0] is '/':
                    continue
                for api in root_path[1]['apis']:
                    self._path_arguments.add_path(api['path'].split('/')[1:])


class _FixedPathArgument(object):
    def __init__(self, path):
        self._subpaths = {}
        self._path = path

    def add_path(self, paths):
        if len(paths) == 0:
            return
        subpath = self._subpaths.get(paths[0], None)
        if subpath is None:
            subpath = _FixedPathArgument(paths[0])
            self._subpaths[paths[0]] = subpath

        subpath.add_path(paths[1:])

    @property
    def path(self):
        return self._path

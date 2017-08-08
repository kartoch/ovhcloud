import json
import logging
import sys
from argparse import ArgumentParser

import ovh
from ovh import Client

import ovhcloud


class GenerateArguments(object):
    def __init__(self, args: str, actions: dict, client: Client):
        self._client = client
        parser = self._build_parser(actions, args)
        self._analyze_args(parser)

    def _analyze_args(self, parser):

        logging.basicConfig(level=getattr(self.args, 'log_level'))

        if self.args.group_or_command is None:
            parser.print_help()
            sys.exit(1)

    def _build_parser(self, actions, args):
        parser = ArgumentParser(prog='ovhcloud')
        self._parse_flags(parser)
        subparsers = parser.add_subparsers(dest="group_or_command")
        self._parse_commands(subparsers, actions)
        self._parse_api(subparsers)
        self._args = parser.parse_args(args)
        return parser

    @property
    def args(self):
        return self._args

    def _parse_flags(self, parser: ArgumentParser):

        # parse log flags
        parser.add_argument(
            '-d', '--debug',
            help="Print lots of debugging statements",
            action="store_const", dest="log_level", const=logging.DEBUG,
            default=logging.WARNING,
        )

        # parse endpoint flag
        parser.add_argument(
            '-e', '--endpoint',
            help="Select the endpoint",
            choices=ovh.client.ENDPOINTS.keys(),
            dest="endpoint",
            default="ovh-eu"
        )

        # parse version flag
        parser.add_argument('-v', '--version', action='version', version=ovhcloud.__version__)

    def _parse_commands(self, subparsers: ArgumentParser, actions: dict):
        for k in actions.keys():
            subparser = subparsers.add_parser(k)
            actions[k].parser(subparser)

    def _parse_api(self, subparsers: ArgumentParser):
        f = open(self._client.cache_file)
        c = json.load(f)

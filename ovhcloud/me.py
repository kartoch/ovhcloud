import logging


class MeGroup(object):
    name = 'me'

    log = logging.getLogger(__name__)

    def parser(self, parser):
        subparsers = parser.add_subparsers(dest="command")
        subparser_add = subparsers.add_parser('add')
        subparser_add.add_argument("name", help="SSH key name")
        subparser_add.add_argument("key", help="SSH key value")
        subparser_rm = subparsers.add_parser('rm')
        subparser_rm.add_argument("name", help="SSH key name")

    def action(self, info):
        c = self.list_commands[info['args'].command]
        c(self, info)

    def _action_me(self, info):
        print(info['client'].get('/me'))

    def _action_add(self, info):
        pass

    def _action_rm(self, info):
        pass

    def _action_default(self, info):
        info['client'].get('/me/sshKey')

    list_commands = {
        'add': _action_add,
        'rm': _action_rm,
        None: _action_default,
    }

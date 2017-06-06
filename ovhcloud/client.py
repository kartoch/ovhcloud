# parser.add_argument("names", help="the vps names separated by comma")
# parser.add_argument('--template', action="store", dest="template", help="template name")
# parser.add_argument('--lang', default="en", action="store", dest="lang", help="template language")
# parser.add_argument('--ssh', action="store", dest="ssh", help="ssh key name")
#
# log = logging.getLogger(__name__)
#
# vps_names = args.names.split(',')
#
# template_name = args.template
# template_lang = args.lang
# ssh_key = args.ssh
# task_refresh = args.wait
#
# client = ovh.Client()
#
# logger.info("Welcome %s", client.get('/me')['firstname'])
#
# if ssh_key:
#     ssh_keys = client.get('/me/sshKey')
#
#     if ssh_key in ssh_keys:
#         logger.info("found ssh key %s", ssh_key)
#     else:
#         logger.error("cannot found ssh key %s", ssh_key)
#         sys.exit(1)
#
# vps = client.get('/vps')
#
# tasks = []
#
# for vps_name in vps_names:
#
#     # check VPS name
#     if vps_name not in vps:
#         logger.error("cannot found vps: %s", vps_name)
#         sys.exit(1)
#     else:
#         logger.info("found vps: %s", vps_name)
#
#     # get all templates
#     template_ids = client.get('/vps/%s/templates' % vps_name)
#     template_id = None
#     for id in template_ids:
#         template_info = client.get('/vps/%s/templates/%s' % (vps_name, id))
#         if template_info['distribution'] == template_name:
#             template_id = template_info['id']
#             if template_lang in template_info['availableLanguage']:
#                 logger.info("found lang %s for template %s", template_lang,
#                             template_name)
#             else:
#                 logger.error("cannot found lang %s for template %s",
#                              template_lang,
#                              template_name)
#                 sys.exit(1)
#             break
#
#     if template_id:
#         logger.info("found template %s, id is %i", template_name, template_id)
#     else:
#         logger.error("cannot found template: %s", template_name)
#         sys.exit(1)
#
#     logger.info("POST reinstall command")
#     # task = client.post('/vps/%s/reinstall' % vps_name,
#     #                    doNotSendPassword=True,
#     #                    templateId=template_id,
#     #                    language=template_lang,
#     #                    sshKey=[ssh_key])
#     # logger.debug("task %s: %s", vps_name, task)
#     # tasks.append(task)

import argparse
import logging
import sys

import ovh

from ovhcloud.command import VersionCommand
from ovhcloud.me import MeGroup


class OVHClient(object):
    log = logging.getLogger(__name__)

    _action_cls = [VersionCommand, MeGroup]
    info = {'actions': {cls.name: cls() for cls in _action_cls}}

    def __init__(self, args):
        self.info['args'] = self._parse_arguments(args)

    def _parse_arguments(self, args):
        parser = argparse.ArgumentParser(prog='ovhcloud')
        subparsers = parser.add_subparsers(dest="group_or_command")
        for k in self.info['actions'].keys():
            subparser = subparsers.add_parser(k)
            self.info['actions'][k].parser(subparser)
        return parser.parse_args(args)

    def action(self):
        # first connect to see if we are authorized
        self._connect()
        # search for the group or the command and call the associated action
        command_cls_action = self.info['actions'].get(self.info['args'].group_or_command)
        command_cls_action.action(self.info)

    def _connect(self):
        self.info['client'] = ovh.Client()


def main():
    client = OVHClient(sys.argv[1:])
    client.action()


if __name__ == '__main__':
    main()

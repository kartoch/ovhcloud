import argparse
import logging
import sys
import time

import ovh

# Configure logger

logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__name__)

# Get arguments

parser = argparse.ArgumentParser()

# mandatory arguments
parser.add_argument("names", help="the vps names separated by comma")
parser.add_argument('--sshkey', action="store", dest="ssh",
                    help="ssh key name")

# optional arguments
parser.add_argument("--template", default="ubuntu1604-server", action="store",
                    dest="template", help="the template name")
parser.add_argument('--lang', default="en", action="store", dest="lang",
                    help="the template language")
parser.add_argument('--wait', default=60, action="store", dest="wait",
                    help="task refresh time")
args = parser.parse_args()

vps_names = args.names.split(',')

template_name = args.template
template_lang = args.lang
ssh_key = args.ssh
task_refresh = args.wait

client = ovh.Client()

logger.info("Welcome %s", client.get('/me')['firstname'])

if ssh_key:
    ssh_keys = client.get('/me/sshKey')

    if ssh_key in ssh_keys:
        logger.info("found ssh key %s", ssh_key)
    else:
        logger.error("cannot found ssh key %s", ssh_key)
        sys.exit(1)

vps = client.get('/vps')

tasks = []

for vps_name in vps_names:

    # check VPS name
    if vps_name not in vps:
        logger.error("cannot found vps: %s", vps_name)
        sys.exit(1)
    else:
        logger.info("found vps: %s", vps_name)

    # get all templates
    template_ids = client.get('/vps/%s/templates' % vps_name)
    template_id = None
    for id in template_ids:
        template_info = client.get('/vps/%s/templates/%s' % (vps_name, id))
        if template_info['distribution'] == template_name:
            template_id = template_info['id']
            if template_lang in template_info['availableLanguage']:
                logger.info("found lang %s for template %s", template_lang,
                            template_name)
            else:
                logger.error("cannot found lang %s for template %s",
                             template_lang,
                             template_name)
                sys.exit(1)
            break

    if template_id:
        logger.info("found template %s, id is %i", template_name, template_id)
    else:
        logger.error("cannot found template: %s", template_name)
        sys.exit(1)

    logger.info("POST reinstall command")
    # task = client.post('/vps/%s/reinstall' % vps_name,
    #                    doNotSendPassword=True,
    #                    templateId=template_id,
    #                    language=template_lang,
    #                    sshKey=[ssh_key])
    # logger.debug("task %s: %s", vps_name, task)
    # tasks.append(task)

while True:
    task_states = []

    for i in range(len(vps_names)):
        n = vps_names[i]
        t = tasks[i]
        state = client.get('/vps/%s/tasks/%i' % (n, t['id']))
        task_states.append(state)
        logger.info("task refresh: %s", t)

    if all(s['state'] == "done" for s in task_states):
        logger.info("all tasks done")
        sys.exit(0)

    time.sleep(task_refresh)

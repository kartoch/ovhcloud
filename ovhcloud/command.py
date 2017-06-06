import logging
import sys

import ovhcloud


class VersionCommand(object):
    name = 'version'

    log = logging.getLogger(__name__)

    def parser(self, parser):
        pass

    def action(self, info):
        print(ovhcloud.__version__)
        sys.exit(0)

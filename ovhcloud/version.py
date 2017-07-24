import ovhcloud
from ovhcloud.commands import Command


class VersionCommand(Command):
    name = 'version'

    def parser(self, parser):
        pass

    def action(self):
        print(ovhcloud.__version__)

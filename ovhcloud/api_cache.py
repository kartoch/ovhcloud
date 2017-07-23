import sys

from ovhcloud.commands import Command


class ApiCacheCommand(Command):
    name = 'cache'

    def parser(self, parser):
        pass

    def action(self):
        self._cache_references()
        sys.exit(0)

    def _download_references(self, path):
        self.log.debug("caching %s " % path)
        json = self._client._ovh_client.get(path)
        return json

    def _cache_references(self):
        main = self._download_references('/')
        for api in main['apis']:
            self._download_references(api['path'] + '.json')

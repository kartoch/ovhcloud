import io
import json
from argparse import ArgumentParser

import ovh

from ovhcloud.commands import Command


class ApiCacheCommand(Command):

    def parser(self, parser: ArgumentParser):
        pass

    def action(self):
        self._cache_references()

    def _download_references(self, path: str, c: ovh.Client):
        self._log.debug("caching %s" % path)
        return c.get(path, _need_auth=False)

    def _download_endpoint(self, endpoint: str):
        self._log.debug("caching endpoint %s" % endpoint)
        c = ovh.Client(endpoint=endpoint)
        content = {
            'timestamp': c.get('/auth/time', _need_auth=False),
            'paths': {}
        }
        path = '/'
        main = self._download_references(path, c)
        content['paths'][path] = main
        for api in main['apis']:
            path = api['path'] + '.json'
            content['paths'][path] = self._download_references(path, c)
        return content

    def _cache_references(self):
        content = {}
        for endpoint in ovh.client.ENDPOINTS.keys():
            content[endpoint] = self._download_endpoint(endpoint)

        with io.open(self._client.cache_file, 'w', encoding='utf8') as f:
            json.dump(content, f)

        self._log.debug("wrote endpoints cache in file %s" % self._client.cache_file)

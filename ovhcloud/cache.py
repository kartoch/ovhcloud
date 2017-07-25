import io
import json
import os

import ovh

from ovhcloud.commands import Command


class ApiCacheCommand(Command):

    name = 'cache'

    DEFAULT_ENDPOINTS_CACHE_FILENAME = 'endpoints_cache.json'

    def parser(self, parser):
        pass

    def action(self):
        return self._cache_references()

    def _download_references(self, path, c):
        self.log.debug("caching %s" % path)
        json = c.get(path, _need_auth=False)
        return json

    def _download_endpoint(self, endpoint):
        self.log.debug("caching endpoint %s" % endpoint)
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

        def compare_content(content, cached_content):
            for e in ovh.client.ENDPOINTS.keys():
                a = content[e]['paths']
                b = cached_content[e]['paths']
                if a != b:
                    return False
            return True

        content = {}
        for endpoint in ovh.client.ENDPOINTS.keys():
            content[endpoint] = self._download_endpoint(endpoint)

        cache_file_path = os.path.join(self._client._configuration_dir, self.DEFAULT_ENDPOINTS_CACHE_FILENAME)

        if os.path.isfile(cache_file_path):
            with io.open(cache_file_path, 'r', encoding='utf8') as f:
                cached_content = json.load(f)
            if compare_content(content, cached_content):
                return False

        with io.open(cache_file_path, 'w', encoding='utf8') as f:
            json.dump(content, f, allow_nan=False)
        self.log.debug("wrote endpoints cache in file %s" % cache_file_path)
        return True

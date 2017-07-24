import ovh

from ovhcloud.commands import Command


class ApiCacheCommand(Command):

    name = 'cache'

    def parser(self, parser):
        pass

    def action(self):
        self._cache_references()

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
        content = {
            'endpoints': {}
        }
        for endpoint in ovh.client.ENDPOINTS.keys():
            content[endpoint] = self._download_endpoint(endpoint)

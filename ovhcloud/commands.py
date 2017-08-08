import logging


class Command(object):

    def __init__(self, client):
        self._client = client

    def set_logging(self):
        self._log = logging.getLogger(__name__)

    def parser(self, parser):
        raise NotImplementedError("parser method not implemented")

    def action(self):
        raise NotImplementedError("action method not implemented")

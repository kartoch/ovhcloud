import logging


class Command(object):
    def __init__(self, client):
        self._client = client

    def set_logging(self):
        self.log = logging.getLogger(__name__)

import ovh
import pytest

from ovhcloud.client import OVHClient

test_data = ovh.client.ENDPOINTS.keys()


@pytest.mark.parametrize("endpoint", test_data)
def test_cache_command(endpoint):
    ovh_client = ovh.Client(endpoint=endpoint)
    with pytest.raises(SystemExit):
        OVHClient(['cache'], ovh_client).action()

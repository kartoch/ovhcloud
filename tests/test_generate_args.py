from unittest.mock import Mock

import ovhcloud
from ovhcloud.client import OVHClient
from ovhcloud.generate_args import GenerateArguments, _FixedPathArgument


def test_build_parser():
    client = Mock(OVHClient)
    client.cache_file = ovhcloud.DEFAULT_ENDPOINTS_API_CACHE
    c = GenerateArguments(client=client)
    actions = {}
    c.build_parser(actions)


def test_build_tree():
    entries = [
        "/dedicated/server",
        "/dedicated/server/availabilities",
        "/dedicatedCloud/{serviceName}/serviceInfos",
        "/dedicatedCloud/{serviceName}/passwordPolicy"
    ]
    f = _FixedPathArgument('/')
    for e in entries:
        f.add_path(e.split('/')[1:])
    assert f.path == '/'
    assert len(f._subpaths) == 2
    assert f._subpaths.get("dedicated", False)
    assert f._subpaths.get("dedicatedCloud", False)
    assert len(f._subpaths["dedicated"]._subpaths) == 1
    assert f._subpaths["dedicated"]._subpaths.get("server", False)
    assert len(f._subpaths["dedicated"]._subpaths["server"]._subpaths) == 1
    assert f._subpaths["dedicated"]._subpaths["server"]._subpaths.get("availabilities", False)
    assert len(f._subpaths["dedicatedCloud"]._subpaths) == 1
    assert f._subpaths["dedicatedCloud"]._subpaths.get("{serviceName}", False)
    assert len(f._subpaths["dedicatedCloud"]._subpaths["{serviceName}"]._subpaths) == 2
    assert f._subpaths["dedicatedCloud"]._subpaths["{serviceName}"]._subpaths.get("serviceInfos", False)
    assert f._subpaths["dedicatedCloud"]._subpaths["{serviceName}"]._subpaths.get("passwordPolicy", False)

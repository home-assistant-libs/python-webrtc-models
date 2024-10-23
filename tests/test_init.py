"""WebRTC models tests."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

from tests import load_fixture
from webrtc_models import RTCConfiguration, RTCIceServer

if TYPE_CHECKING:
    from mashumaro.mixins.orjson import DataClassORJSONMixin
    from syrupy import SnapshotAssertion


@pytest.mark.parametrize(
    ("clazz", "filename"),
    [
        # RTCIceServer
        (RTCIceServer, "RTCIceServer_only_urls_string.json"),
        (RTCIceServer, "RTCIceServer_only_urls_list.json"),
        (RTCIceServer, "RTCIceServer_urls_string.json"),
        (RTCIceServer, "RTCIceServer_urls_list.json"),
        # RTCConfiguration
        (RTCConfiguration, "RTCConfiguration_empty.json"),
        (RTCConfiguration, "RTCConfiguration_one_iceServer.json"),
        (RTCConfiguration, "RTCConfiguration_multiple_iceServers.json"),
    ],
)
def test_decoding_and_encoding(
    snapshot: SnapshotAssertion,
    clazz: type[DataClassORJSONMixin],
    filename: str,
) -> None:
    """Test decoding/encoding."""
    # Json section
    file_content = load_fixture(filename)
    ice_server = clazz.from_json(file_content)
    assert ice_server == snapshot(name="dataclass")
    # replace spaces and newlines
    assert ice_server.to_json() == re.sub(r"\s", "", file_content)

    # Dict section
    ice_server_dict = ice_server.to_dict()
    assert ice_server_dict == snapshot(name="dict")
    assert ice_server == clazz.from_dict(ice_server_dict)

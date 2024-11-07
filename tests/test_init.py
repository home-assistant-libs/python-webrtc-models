"""WebRTC models tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import orjson
import pytest

from tests import load_fixture
from webrtc_models import RTCConfiguration, RTCIceCandidate, RTCIceServer

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
        # RTCIceCandidate
        (RTCIceCandidate, "RTCIceCandidate_end.json"),
        (RTCIceCandidate, "RTCIceCandidate_candidate.json"),
    ],
)
def test_decoding_and_encoding(
    snapshot: SnapshotAssertion,
    clazz: type[DataClassORJSONMixin],
    filename: str,
) -> None:
    """Test decoding/encoding."""
    file_content = load_fixture(filename)
    instance = clazz.from_json(file_content)
    assert instance == snapshot(name="dataclass")

    file_content_dict = orjson.loads(file_content)
    instance_dict = instance.to_dict()
    assert instance_dict == snapshot(name="dict")

    # Verify json
    assert instance.to_json() == orjson.dumps(file_content_dict).decode()

    # Verify dict
    assert instance_dict == file_content_dict
    assert instance == clazz.from_dict(instance_dict)


def test_no_mid_and_mlineindex() -> None:
    """Test spd_mid and sdp_multilineindex raises TypeError."""
    file_content = load_fixture("RTCIceCandidate_invalid.json")
    with pytest.raises(TypeError):
        RTCIceCandidate.from_json(file_content)


def test_empty_candidate_creation() -> None:
    """Test empty candidate creation."""
    file_content = load_fixture("RTCIceCandidate_end.json")
    file_content_dict = orjson.loads(file_content)
    rtc_ice_end = RTCIceCandidate()
    assert rtc_ice_end.to_dict() == file_content_dict

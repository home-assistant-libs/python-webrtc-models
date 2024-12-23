"""WebRTC models tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import orjson
import pytest

from tests import load_fixture
from webrtc_models import (
    RTCConfiguration,
    RTCIceCandidate,
    RTCIceCandidateInit,
    RTCIceServer,
)

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
        # RTCIceCandidateInit
        (RTCIceCandidateInit, "RTCIceCandidateInit_end.json"),
        (RTCIceCandidateInit, "RTCIceCandidateInit_candidate.json"),
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

    # Verify json
    assert instance.to_json() == orjson.dumps(file_content_dict).decode()

    # Verify dict
    assert instance_dict == file_content_dict
    assert instance == clazz.from_dict(instance_dict)


@pytest.mark.parametrize(
    ("clazz", "filename"),
    [
        # RTCIceCandidate
        (RTCIceCandidate, "RTCIceCandidate_end.json"),
        (RTCIceCandidate, "RTCIceCandidate_candidate.json"),
    ],
)
def test_decoding_and_encoding_deprecated(
    snapshot: SnapshotAssertion,
    clazz: type[DataClassORJSONMixin],
    filename: str,
) -> None:
    """Test decoding/encoding."""
    file_content = load_fixture(filename)
    with pytest.deprecated_call():
        instance = clazz.from_json(file_content)
    assert instance == snapshot(name="dataclass")

    file_content_dict = orjson.loads(file_content)
    instance_dict = instance.to_dict()

    # Verify json
    assert instance.to_json() == orjson.dumps(file_content_dict).decode()

    # Verify dict
    assert instance_dict == file_content_dict
    with pytest.deprecated_call():
        assert instance == clazz.from_dict(instance_dict)


def test_no_mid_and_mlineindex() -> None:
    """Test spd_mid and sdp_multilineindex raises TypeError."""
    file_content = load_fixture("RTCIceCandidate_candidate.json")
    cand = RTCIceCandidateInit.from_json(file_content)
    assert cand.sdp_m_line_index == 0
    assert cand.sdp_mid is None


def test_invalid_mlineindex() -> None:
    """Test spd_mid and sdp_multilineindex raises TypeError."""
    file_content = load_fixture("RTCIceCandidateInit_invalid.json")
    msg = "sdpMLineIndex must be greater than or equal to 0"
    with pytest.raises(ValueError, match=msg):
        RTCIceCandidateInit.from_json(file_content)

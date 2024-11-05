"""WebRTC models."""

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin

__all__ = [
    "RTCConfiguration",
    "RTCIceCandidate",
    "RTCIceServer",
]


class _RTCBaseModel(DataClassORJSONMixin):
    """Base class for RTC models."""

    class Config(BaseConfig):
        """Mashumaro config."""

        # Serialize to spec conform names and omit default values
        omit_default = True
        serialize_by_alias = True


@dataclass
class RTCIceServer(_RTCBaseModel):
    """RTC Ice Server.

    See https://www.w3.org/TR/webrtc/#rtciceserver-dictionary
    """

    urls: str | list[str]
    username: str | None = None
    credential: str | None = None


@dataclass
class RTCConfiguration(_RTCBaseModel):
    """RTC Configuration.

    See https://www.w3.org/TR/webrtc/#rtcconfiguration-dictionary
    """

    ice_servers: list[RTCIceServer] = field(
        metadata=field_options(alias="iceServers"), default_factory=list
    )


@dataclass(frozen=True)
class RTCIceCandidate(_RTCBaseModel):
    """RTC Ice Candidate.

    See https://www.w3.org/TR/webrtc/#rtcicecandidate-interface
    """

    candidate: str
    sdp_m_line_index: int

"""WebRTC models."""

from dataclasses import dataclass, field
from warnings import warn

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

    def __post_init__(self) -> None:
        """Initialize class."""
        msg = "Using RTCIceCandidate is deprecated. Use RTCIceCandidateInit instead"
        warn(msg, DeprecationWarning, stacklevel=2)


@dataclass(frozen=True)
class RTCIceCandidateInit(RTCIceCandidate):
    """RTC Ice Candidate Init.

    See https://www.w3.org/TR/webrtc/#dom-rtcicecandidateinit
    """

    candidate: str
    sdp_mid: str | None = field(
        metadata=field_options(alias="sdpMid"), default=None, kw_only=True
    )
    sdp_m_line_index: int | None = field(
        metadata=field_options(alias="sdpMLineIndex"), default=None, kw_only=True
    )
    user_fragment: str | None = field(
        metadata=field_options(alias="userFragment"), default=None, kw_only=True
    )

    def __post_init__(self) -> None:
        """Initialize class.

        Spec compliance: If both the sdpMid and sdpMLineIndex members of
        candidateInitDict are null, throw a TypeError.
        """
        if (
            self.candidate != ""
            and self.sdp_mid is None
            and self.sdp_m_line_index is None
        ):
            msg = "sdpMid or sdpMLineIndex must be set"
            raise TypeError(msg)

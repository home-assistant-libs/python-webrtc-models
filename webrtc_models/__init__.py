"""WebRTC models."""

from dataclasses import dataclass, field
from typing import Any

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
class RTCIceCandidateInit(_RTCBaseModel):
    """RTC Ice Candidate Init.

    See https://www.w3.org/TR/webrtc/#rtcicecandidate-interface
    """

    candidate: str
    sdp_m_line_index: int | None = field(
        metadata=field_options(alias="sdpMLineIndex"), default=None, kw_only=True
    )
    sdp_mid: str | None = field(
        metadata=field_options(alias="sdpMid"), default=None, kw_only=True
    )
    user_fragment: str | None = field(
        metadata=field_options(alias="userFragment"), default=None, kw_only=True
    )


@dataclass(frozen=True)
class RTCIceCandidate(_RTCBaseModel):
    """RTC Ice Candidate.

    See https://www.w3.org/TR/webrtc/#rtcicecandidate-interface
    """

    class Config(BaseConfig):
        """Mashumaro config."""

        # Serialize to spec conform names and omit default values
        omit_default = False
        serialize_by_alias = True

    rtc_ice_candidate_init: RTCIceCandidateInit | None = field(
        default=None, metadata=field_options(serialize="omit")
    )

    candidate: str = field(init=False)
    sdp_m_line_index: int | None = field(
        metadata=field_options(alias="sdpMLineIndex"), default=None, init=False
    )
    sdp_mid: str | None = field(
        metadata=field_options(alias="sdpMid"), default=None, init=False
    )
    user_fragment: str | None = field(
        metadata=field_options(alias="userFragment"), default=None, init=False
    )

    foundation: str | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )
    component: str | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )
    priority: int | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )
    address: str | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )
    protocol: str | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )
    port: int | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )
    type: str | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )
    tcp_type: str | None = field(
        metadata=field_options(alias="tcpType", serialize="omit"),
        default=None,
        init=False,
    )
    related_address: str | None = field(
        metadata=field_options(alias="relatedAddress", serialize="omit"),
        default=None,
        init=False,
    )
    related_port: str | None = field(
        metadata=field_options(alias="relatedPort", serialize="omit"),
        default=None,
        init=False,
    )

    relay_protocol: str | None = field(
        metadata=field_options(alias="relayProtocol", serialize="omit"),
        default=None,
        init=False,
    )
    url: str | None = field(
        default=None, init=False, metadata=field_options(serialize="omit")
    )

    @classmethod
    def __pre_deserialize__(cls, d: dict[Any, Any]) -> dict[Any, Any]:
        """Per spec candidate serializes and deserialises to/from RTCIceCAndidateInit.

        To invoke the toJSON() operation of the RTCIceCandidate interface,
        run the following steps:
        1. Let json be a new RTCIceCandidateInit dictionary.
        2. For each attribute identifier attr in candidate, sdpMid,
            sdpMLineIndex, usernameFragment:
        3. Let value be the result of getting the underlying value of the attribute
            identified by attr, given this RTCIceCandidate object.
        4. Set json[attr] to value.
        5. Return json.

        This method reverses that logic.
        """
        candidate_init = RTCIceCandidateInit.from_dict(d)
        return {"rtc_ice_candidate_init": candidate_init.to_dict()}

    def __post_init__(self) -> None:
        """Initialize the class.

        Spec compliance: If both the sdpMid and sdpMLineIndex members of
        candidateInitDict are null, throw a TypeError.
        """
        ric_init = self.rtc_ice_candidate_init
        if (
            ric_init
            and ric_init.candidate != ""
            and ric_init.sdp_m_line_index is None
            and ric_init.sdp_mid is None
        ):
            msg = "sdp_m_line_index and sdp_mid cannot both be null."
            raise TypeError(msg)

        if ric_init:
            # Attributes are readonly so set them via __setattr__
            object.__setattr__(self, "candidate", ric_init.candidate)
            object.__setattr__(self, "sdp_mid", ric_init.sdp_mid)
            object.__setattr__(self, "sdp_m_line_index", ric_init.sdp_m_line_index)
            object.__setattr__(self, "user_fragment", ric_init.user_fragment)
        else:
            object.__setattr__(self, "candidate", "")

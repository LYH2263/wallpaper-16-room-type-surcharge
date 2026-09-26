"""Wet-room rule: add a fixed number of rolls on top of base rolls."""
from __future__ import annotations

from dataclasses import dataclass

from app.modules.wet_room.types import DEFAULT_SPACE_TYPE, SpaceType

SETTING_ENABLED = "wet_room_enabled"
SETTING_EXTRA_ROLLS = "wet_room_extra_rolls"

DEFAULT_ENABLED = True
DEFAULT_EXTRA_ROLLS = 1

_TRUE = {"true", "1", "yes", "on"}
_FALSE = {"false", "0", "no", "off"}


def parse_enabled(raw: str | None) -> bool:
    if raw is None:
        return DEFAULT_ENABLED
    token = raw.strip().lower()
    if token in _TRUE:
        return True
    if token in _FALSE:
        return False
    raise ValueError(f"invalid boolean setting: {raw!r}")


def parse_extra_rolls(raw: str | None) -> int:
    if raw is None:
        return DEFAULT_EXTRA_ROLLS
    value = int(str(raw).strip())
    if value < 0:
        raise ValueError("extra rolls must be non-negative")
    return value


@dataclass(frozen=True)
class WetRoomSettings:
    enabled: bool = DEFAULT_ENABLED
    extra_rolls: int = DEFAULT_EXTRA_ROLLS

    @classmethod
    def from_map(cls, raw: dict[str, str] | None) -> "WetRoomSettings":
        raw = raw or {}
        return cls(
            parse_enabled(raw.get(SETTING_ENABLED)),
            parse_extra_rolls(raw.get(SETTING_EXTRA_ROLLS)),
        )


def apply_wet_room_rule(
    space_type: SpaceType | str,
    base_rolls: int,
    *,
    enabled: bool,
    extra_rolls: int,
) -> dict:
    st = SpaceType(space_type)
    if extra_rolls < 0:
        raise ValueError("extra rolls must be non-negative")
    active = st is SpaceType.WET and enabled
    added = extra_rolls if active else 0
    return {
        "space_type": st.value,
        "base_rolls": int(base_rolls),
        "order_rolls": int(base_rolls) + added,
        "wet_extra_applied": active and extra_rolls > 0,
    }

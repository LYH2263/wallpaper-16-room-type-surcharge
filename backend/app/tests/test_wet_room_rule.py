import pytest

from app.modules.wet_room.rule import (
    DEFAULT_ENABLED,
    DEFAULT_EXTRA_ROLLS,
    WetRoomSettings,
    apply_wet_room_rule,
    parse_enabled,
    parse_extra_rolls,
)
from app.modules.wet_room.types import DEFAULT_SPACE_TYPE, SpaceType


def test_normal_returns_base():
    out = apply_wet_room_rule(SpaceType.NORMAL, 11, enabled=True, extra_rolls=2)
    assert out == {
        "space_type": "normal",
        "base_rolls": 11,
        "order_rolls": 11,
        "wet_extra_applied": False,
    }


def test_wet_enabled_adds_fixed_rolls():
    out = apply_wet_room_rule("wet", 11, enabled=True, extra_rolls=2)
    assert out["space_type"] == "wet"
    assert out["base_rolls"] == 11
    assert out["order_rolls"] == 13
    assert out["wet_extra_applied"] is True


def test_wet_disabled_falls_back_to_base():
    out = apply_wet_room_rule(SpaceType.WET, 11, enabled=False, extra_rolls=2)
    assert out["order_rolls"] == 11
    assert out["wet_extra_applied"] is False


def test_extra_zero_means_no_surcharge():
    out = apply_wet_room_rule(SpaceType.WET, 11, enabled=True, extra_rolls=0)
    assert out["order_rolls"] == 11
    assert out["wet_extra_applied"] is False


def test_unknown_type_raises():
    with pytest.raises(ValueError):
        apply_wet_room_rule("steam", 11, enabled=True, extra_rolls=1)


def test_negative_extra_raises():
    with pytest.raises(ValueError):
        apply_wet_room_rule(SpaceType.WET, 11, enabled=True, extra_rolls=-1)


def test_settings_from_explicit_map():
    cfg = WetRoomSettings.from_map(
        {"wet_room_enabled": "false", "wet_room_extra_rolls": "3"}
    )
    assert cfg.enabled is False
    assert cfg.extra_rolls == 3


def test_settings_from_empty_map_uses_defaults():
    cfg = WetRoomSettings.from_map({})
    assert cfg.enabled is DEFAULT_ENABLED
    assert cfg.extra_rolls == DEFAULT_EXTRA_ROLLS


def test_settings_from_none_uses_defaults():
    cfg = WetRoomSettings.from_map(None)
    assert cfg.enabled is True
    assert cfg.extra_rolls == 1


def test_parse_enabled_variants():
    assert parse_enabled("true") is True
    assert parse_enabled("1") is True
    assert parse_enabled("OFF") is False
    assert parse_enabled("0") is False
    with pytest.raises(ValueError):
        parse_enabled("maybe")


def test_parse_extra_rolls_rejects_bad_values():
    assert parse_extra_rolls("2") == 2
    with pytest.raises(ValueError):
        parse_extra_rolls("-1")
    with pytest.raises(ValueError):
        parse_extra_rolls("abc")


def test_enum_and_default():
    assert SpaceType("wet") is SpaceType.WET
    assert SpaceType.WET.value == "wet"
    assert DEFAULT_SPACE_TYPE is SpaceType.NORMAL
    # str mixin: values compare/serialize as plain strings
    assert SpaceType.WET == "wet"

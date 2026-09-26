from fastapi import APIRouter
from app.modules.wet_room.rule import (
    SETTING_ENABLED,
    SETTING_EXTRA_ROLLS,
    WetRoomSettings,
)
from app.repositories import settings_repo
from app.schemas.settings import SettingsUpdate

router = APIRouter()


def _payload(raw: dict) -> dict:
    cfg = WetRoomSettings.from_map(raw)
    return {
        **raw,
        SETTING_ENABLED: cfg.enabled,
        SETTING_EXTRA_ROLLS: cfg.extra_rolls,
    }


@router.get("/settings")
def settings():
    return _payload(settings_repo.get_all())


@router.put("/settings")
def update_settings(body: SettingsUpdate):
    values = {}
    if body.wet_room_enabled is not None:
        values[SETTING_ENABLED] = "true" if body.wet_room_enabled else "false"
    if body.wet_room_extra_rolls is not None:
        values[SETTING_EXTRA_ROLLS] = str(body.wet_room_extra_rolls)
    if values:
        settings_repo.upsert_many(values)
    return _payload(settings_repo.get_all())

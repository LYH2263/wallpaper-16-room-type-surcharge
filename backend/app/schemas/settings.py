from pydantic import BaseModel, ConfigDict, Field


class SettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    wet_room_enabled: bool | None = None
    wet_room_extra_rolls: int | None = Field(default=None, ge=0)

from pydantic import BaseModel

from app.modules.wet_room.types import SpaceType


class WallTypeUpdate(BaseModel):
    space_type: SpaceType

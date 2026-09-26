"""Wall space type enum: normal rooms vs wet/humid rooms."""
from enum import Enum


class SpaceType(str, Enum):
    NORMAL = "normal"  # 普通
    WET = "wet"        # 潮湿


DEFAULT_SPACE_TYPE = SpaceType.NORMAL

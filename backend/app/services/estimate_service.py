from fastapi import HTTPException

from app.engines.wallpaper_math import roll_count
from app.modules.wet_room.rule import WetRoomSettings, apply_wet_room_rule
from app.modules.wet_room.types import DEFAULT_SPACE_TYPE
from app.repositories import history, rolls, settings_repo, walls


def run_estimate(wall_id: int, roll_id: int, save: bool, note: str):
    wall = walls.get_wall(wall_id)
    if not wall:
        raise HTTPException(404, "wall not found")
    roll = rolls.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    if wall.get("data_quality") == "dirty" or roll.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty seed entity")

    calc = roll_count(
        wall["perimeter"], wall["height"], roll["width"], roll["length"], roll["pattern_cm"]
    )
    cfg = WetRoomSettings.from_map(settings_repo.get_all())
    wet = apply_wet_room_rule(
        wall.get("space_type") or DEFAULT_SPACE_TYPE.value,
        calc["rolls"],
        enabled=cfg.enabled,
        extra_rolls=cfg.extra_rolls,
    )
    snapshot = {**calc, **wet, "wall_id": wall_id, "roll_id": roll_id}
    run_id = None
    if save:
        run_id = history.insert_run(wall_id, roll_id, snapshot, note)
    return {"wall": wall, "roll": roll, "run_id": run_id, **snapshot}

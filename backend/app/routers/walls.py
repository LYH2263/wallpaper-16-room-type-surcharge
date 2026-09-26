from fastapi import APIRouter, HTTPException
from app.repositories import walls as repo
from app.schemas.wall import WallTypeUpdate

router = APIRouter()


@router.get("/walls")
def list_walls():
    return {"items": repo.list_walls()}


@router.get("/walls/{wall_id}")
def get_wall(wall_id: int):
    row = repo.get_wall(wall_id)
    if not row:
        raise HTTPException(404)
    return row


@router.patch("/walls/{wall_id}")
def patch_wall(wall_id: int, body: WallTypeUpdate):
    row = repo.update_space_type(wall_id, body.space_type.value)
    if not row:
        raise HTTPException(404)
    return row

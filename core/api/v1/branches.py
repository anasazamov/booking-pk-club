from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.location import (
    BranchRead, BranchCreate, BranchUpdate,
    ZoneRead, ZoneCreate, ZoneUpdate,
    PlaceRead, PlaceCreate, PlaceUpdate
)
from core.crud.location import (
    list_branches, get_branch, create_branch, update_branch, delete_branch,
    list_zones, get_zone, create_zone, update_zone, delete_zone,
    list_places, get_place, create_place, update_place, delete_place
)
from core.api.deps import get_current_user
from core.database.models.models import RoleEnum
from core.database.db_helper import db_helper
get_db = db_helper.scoped_session_dependency

router = APIRouter(prefix="", tags=["location"])


@router.get(
    "/branches",
    response_model=List[BranchRead]
)
async def get_branches(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    db: AsyncSession = Depends(get_db)
):

    all_branches = await list_branches(db)
    return all_branches[skip : skip + limit]

@router.post(
    "/branches",
    response_model=BranchRead,
    status_code=status.HTTP_201_CREATED
)
async def post_branch(
    data: BranchCreate,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):

    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await create_branch(db, data)

@router.get(
    "/branches/{branch_id}",
    response_model=BranchRead
)
async def get_branch_detail(
    branch_id: int,
    db: AsyncSession = Depends(get_db)
):

    branch = await get_branch(db, branch_id)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return branch

@router.put(
    "/branches/{branch_id}",
    response_model=BranchRead
)
async def put_branch(
    branch_id: int,
    data: BranchUpdate,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):

    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    branch = await update_branch(db, branch_id, data)
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
    return branch

@router.delete(
    "/branches/{branch_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def del_branch(
    branch_id: int,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):

    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    await delete_branch(db, branch_id)

# Zone endpoints
@router.get(
    "/zones",
    response_model=List[ZoneRead]
)
async def get_zones(
    branch_id: int = Query(..., ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):

    zones = await list_zones(db, branch_id)
    return zones[skip : skip + limit]

@router.post(
    "/zones",
    response_model=ZoneRead,
    status_code=status.HTTP_201_CREATED
)
async def post_zone(
    data: ZoneCreate,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):

    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await create_zone(db, data)

@router.get(
    "/zones/{zone_id}",
    response_model=ZoneRead
)
async def get_zone_detail(
    zone_id: int,
    db: AsyncSession = Depends(get_db)
):

    zone = await get_zone(db, zone_id)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zone not found")
    return zone

@router.put(
    "/zones/{zone_id}",
    response_model=ZoneRead
)
async def put_zone(
    zone_id: int,
    data: ZoneUpdate,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):

    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    zone = await update_zone(db, zone_id, data)
    if not zone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zone not found")
    return zone

@router.delete(
    "/zones/{zone_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def del_zone(
    zone_id: int,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):

    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    await delete_zone(db, zone_id)

# Place endpoints
@router.get(
    "/places",
    response_model=List[PlaceRead]
)
async def get_places(
    zone_id: int = Query(..., ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):

    places = await list_places(db, zone_id)
    return places[skip : skip + limit]

@router.post(
    "/places",
    response_model=PlaceRead,
    status_code=status.HTTP_201_CREATED
)
async def post_place(
    data: PlaceCreate,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):

    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await create_place(db, data)

@router.get(
    "/places/{place_id}",
    response_model=PlaceRead
)
async def get_place_detail(
    place_id: int,
    db: AsyncSession = Depends(get_db)
):

    place = await get_place(db, place_id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place

@router.put(
    "/places/{place_id}",
    response_model=PlaceRead
)
async def put_place(
    place_id: int,
    data: PlaceUpdate,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):
  
    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    place = await update_place(db, place_id, data)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place

@router.delete(
    "/places/{place_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def del_place(
    place_id: int,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user)
):
   
    if current.role not in (RoleEnum.ADMIN, RoleEnum.OWNER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    await delete_place(db, place_id)
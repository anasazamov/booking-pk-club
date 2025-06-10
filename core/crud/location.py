from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database.models.models import Branch, Zone, Place
from core.schemas.location import (
    BranchCreate, BranchUpdate,
    ZoneCreate, ZoneUpdate,
    PlaceCreate, PlaceUpdate
)

async def list_branches(db: AsyncSession) -> list[Branch]:
    result = await db.execute(select(Branch))
    return result.scalars().all()

async def get_branch(db: AsyncSession, branch_id: int) -> Branch | None:
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    return result.scalar_one_or_none()

async def create_branch(db: AsyncSession, data: BranchCreate) -> Branch:
    branch = Branch(**data.model_dump())
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch

async def update_branch(db: AsyncSession, branch_id: int, data: BranchUpdate) -> Branch | None:
    branch = await get_branch(db, branch_id)
    if not branch:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(branch, field, value)
    await db.commit()
    await db.refresh(branch)
    return branch

async def delete_branch(db: AsyncSession, branch_id: int) -> None:
    branch = await get_branch(db, branch_id)
    if branch:
        await db.delete(branch)
        await db.commit()

async def list_zones(db: AsyncSession, branch_id: int) -> list[Zone]:
    result = await db.execute(select(Zone).where(Zone.branch_id == branch_id))
    return result.scalars().all()

async def get_zone(db: AsyncSession, zone_id: int) -> Zone | None:
    result = await db.execute(select(Zone).where(Zone.id == zone_id))
    return result.scalar_one_or_none()

async def create_zone(db: AsyncSession, data: ZoneCreate) -> Zone:
    zone = Zone(**data.model_dump())
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone

async def update_zone(db: AsyncSession, zone_id: int, data: ZoneUpdate) -> Zone | None:
    zone = await get_zone(db, zone_id)
    if not zone:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(zone, field, value)
    await db.commit()
    await db.refresh(zone)
    return zone

async def delete_zone(db: AsyncSession, zone_id: int) -> None:
    zone = await get_zone(db, zone_id)
    if zone:
        await db.delete(zone)
        await db.commit()

async def list_places(db: AsyncSession, zone_id: int) -> list[Place]:
    result = await db.execute(select(Place).where(Place.zone_id == zone_id))
    return result.scalars().all()

async def get_place(db: AsyncSession, place_id: int) -> Place | None:
    result = await db.execute(select(Place).where(Place.id == place_id))
    return result.scalar_one_or_none()

async def create_place(db: AsyncSession, data: PlaceCreate) -> Place:
    place = Place(**data.model_dump())
    db.add(place)
    await db.commit()
    await db.refresh(place)
    return place

async def update_place(db: AsyncSession, place_id: int, data: PlaceUpdate) -> Place | None:
    place = await get_place(db, place_id)
    if not place:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(place, field, value)
    await db.commit()
    await db.refresh(place)
    return place

async def delete_place(db: AsyncSession, place_id: int) -> None:
    place = await get_place(db, place_id)
    if place:
        await db.delete(place)
        await db.commit()
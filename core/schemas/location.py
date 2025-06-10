from pydantic import BaseModel, Field
from typing import Optional

class BranchBase(BaseModel):
    name: str = Field(..., example="Downtown Branch")
    address: Optional[str] = Field(None, example="123 Main St")

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Downtown Branch")
    address: Optional[str] = Field(None, example="123 Main St")

class BranchRead(BranchBase):
    id: int
    class Config:
        orm_mode = True

class ZoneBase(BaseModel):
    name: str = Field(..., example="Zone A")

class ZoneCreate(ZoneBase):
    branch_id: int = Field(..., ge=1)

class ZoneUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Zone A")

class ZoneRead(ZoneBase):
    id: int
    branch_id: int
    class Config:
        orm_mode = True

class PlaceBase(BaseModel):
    name: str = Field(..., example="Seat 1")

class PlaceCreate(PlaceBase):
    zone_id: int = Field(..., ge=1)

class PlaceUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Seat 1")

class PlaceRead(PlaceBase):
    id: int
    zone_id: int
    class Config:
        orm_mode = True
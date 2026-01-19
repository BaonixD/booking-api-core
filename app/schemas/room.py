from pydantic import BaseModel, ConfigDict
from typing import Optional


class RoomCreate(BaseModel):
    hotel_id: int
    name: str
    description: Optional[str] = None
    price: int
    services: Optional[list[str]] = None
    quantity: int
    image_id: Optional[int] = None

class RoomResponse(RoomCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    services: Optional[list[str]] = None
    quantity: Optional[int] = None
    image_id: Optional[int] = None
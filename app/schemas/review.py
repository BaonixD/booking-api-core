from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    rating: int = Field( ge=1, le=5 )
    comment: Optional[str] = None


class ReviewCreate( ReviewBase ):
    hotel_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5 )
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    hotel_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
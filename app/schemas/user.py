from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Базовые поля пользователя"""
    first_name: str = Field(min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: str

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)

class UserUpdate(BaseModel):
    # Делаем всё Optional, чтобы можно было обновлять только одно поле
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "email": "ivan@example.com",
                "created_at": "2026-01-18T12:00:00", # Пример в формате ISO
                "updated_at": None
            }
        }
    )
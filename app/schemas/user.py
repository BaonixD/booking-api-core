from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Базовые поля пользователя (общие для всех схем)"""
    first_name: str = Field(min_length=1, max_length=100, description="Имя пользователя")
    last_name: Optional[str] = Field(None, max_length=100, description="Фамилия пользователя")
    email: EmailStr = Field(description="Электронная почта")

class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Пароль. Минимум 8 символов",
    )

class UserUpdate(UserBase):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)


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
from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import date
from decimal import Decimal
from typing import Optional

# Базовая схема: тут описываем только то, что общее для всех (заезд, выезд, ID комнаты)
class BookingBase(BaseModel):
    room_id: int = Field(..., gt=0, description="На какую комнату падает бронь")
    date_from: date = Field(..., description="День заезда")
    date_to: date = Field(..., description="День выезда")

    @model_validator(mode='after')
    def check_dates(self) -> 'BookingBase':
        # Проверяем логику дат: нельзя уехать раньше, чем заехал
        if self.date_to <= self.date_from:
            raise ValueError('Дата выезда должна быть строго позже даты заезда')

        # Защита от бронирования "задним числом"
        if self.date_from < date.today():
            raise ValueError('Нельзя забронировать номер на прошедшую дату')

        return self


# Эту схему используем в POST-запросе. user_id не просим, вытащим его сами из JWT
class BookingCreate(BookingBase):
    pass


# Админский вариант: если нужно вручную закинуть бронь на конкретного юзера
class BookingCreateAdmin(BookingBase):
    user_id: int = Field(..., gt=0)


# Для PATCH-запросов: тут всё опционально, чтобы можно было обновить только одну дату
class BookingUpdate(BaseModel):
    date_from: Optional[date] = None
    date_to: Optional[date] = None

    @model_validator(mode='after')
    def check_update_dates(self) -> 'BookingUpdate':
        # Если прилетели обе даты, снова проверяем их между собой
        if self.date_from and self.date_to:
            if self.date_to <= self.date_from:
                raise ValueError('Дата выезда должна быть позже даты заезда')
        return self


# --- Вспомогательные схемы для ответов (чтобы фронтенд получал не просто ID, а инфу) ---

class UserShortResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class HotelShortResponse(BaseModel):
    id: int
    name: str
    location: str
    stars: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class RoomShortResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    model_config = ConfigDict(from_attributes=True)


class RoomWithHotelResponse(RoomShortResponse):
    hotel: HotelShortResponse


# --- Основные схемы ответов (то, что летит клиенту) ---

class BookingResponse(BaseModel):
    """Стандартный ответ: информация о бронировании и расчетах"""
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: Decimal
    total_days: int
    total_cost: Decimal

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "room_id": 5,
                "user_id": 10,
                "date_from": "2026-06-01",
                "date_to": "2026-06-05",
                "price": 5500.00,
                "total_days": 4,
                "total_cost": 22000.00
            }
        }
    )


class BookingFullResponse(BookingResponse):
    """Расширенный ответ: со всеми данными о юзере, комнате и отеле"""
    user: UserShortResponse
    room: RoomWithHotelResponse
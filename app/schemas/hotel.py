from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.schemas.room import RoomResponse

# базовая схема
class HotelBase(BaseModel):
    """Базовые поля отеля (общие для создания и чтения)"""
    name: str = Field(..., min_length=1, max_length=200, description="Название отеля")
    location: str = Field(..., min_length=1, max_length=500, description="Адрес отеля")
    services: Optional[list[str]] = Field(default=None, description="Список услуг")
    stars: Optional[int] = Field(default=None, ge=1, le=5, description="Количество звезд (1-5)")
    rooms_quantity: int = Field(..., ge=1, description="Количество номеров")
    image_id: Optional[int] = Field(default=None, description="ID изображения")


class HotelCreate(HotelBase):
    """Схема для создания отеля"""
    pass  # Все поля унаследованы от HotelBase


# обновление
class HotelUpdate(BaseModel):
    """Схема для обновления отеля (все поля опциональны)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=500)
    services: Optional[list[str]] = None
    stars: Optional[int] = Field(None, ge=1, le=5)
    rooms_quantity: Optional[int] = Field(None, ge=1)
    image_id: Optional[int] = None


# полная информация
class HotelResponse(HotelBase):
    """Схема ответа с полной информацией об отеле"""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Гранд Отель",
                "location": "Москва, ул. Тверская, 15",
                "services": ["Wi-Fi", "Парковка", "Бассейн", "Ресторан"],
                "stars": 5,
                "rooms_quantity": 120,
                "image_id": 42
            }
        }
    )


# упрощенная версия
class HotelListResponse(BaseModel):
    """Схема для списка отелей (без лишних деталей)"""
    id: int
    name: str
    location: str
    stars: Optional[int]
    rooms_quantity: int
    image_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


# С КОМНАТАМИ (для подробного просмотра)
class RoomShortResponse(BaseModel):
    """Краткая информация о комнате"""
    id: int
    name: str
    price: int

    model_config = ConfigDict(from_attributes=True)


class HotelWithRoomsResponse(HotelResponse):
    """Схема отеля с его комнатами"""
    rooms: list[RoomResponse] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Гранд Отель",
                "location": "Толе Би 777",
                "services": ["Wi-Fi", "Парковка"],
                "stars": 5,
                "rooms_quantity": 120,
                "image_id": 42,
                "rooms": [
                    {"id": 1, "name": "Стандартный номер", "price": 5000},
                    {"id": 2, "name": "Люкс", "price": 15000}
                ]
            }
        }
    )


# ========== ФИЛЬТРЫ ДЛЯ ПОИСКА ==========
class HotelFilter(BaseModel):
    """Схема для фильтрации отелей"""
    location: Optional[str] = Field(None, description="Поиск по адресу")
    stars: Optional[int] = Field(None, ge=1, le=5, description="Фильтр по звездам")
    min_price: Optional[int] = Field(None, ge=0, description="Минимальная цена")
    max_price: Optional[int] = Field(None, ge=0, description="Максимальная цена")
    services: Optional[list[str]] = Field(None, description="Требуемые услуги")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "location": "Шымкент",
                "stars": 4,
                "min_price": 3000,
                "max_price": 10000,
                "services": ["Wi-Fi", "Парковка"]
            }
        }
    )


class HotelSearchResponse(BaseModel):
    id: int
    name: str
    location: str
    stars: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)

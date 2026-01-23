from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.hotels import get_all_hotels, get_hotel_by_id, create_hotel, delete_hotel, update_hotel, get_hotel_full_info, search_hotels_by_availability
from app.schemas.hotel import HotelResponse, HotelListResponse, HotelCreate, HotelUpdate, HotelWithRoomsResponse, HotelSearchResponse
from datetime import date
from app.crud.user import get_current_user, get_current_admin
from app.models.User import User

router = APIRouter( prefix="/hotels", tags=["Hotels"] )

@router.get( "/", response_model= list[HotelListResponse] )
async def get_hotels( db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user) ):
    return await get_all_hotels(db)


@router.get( "/search", response_model=list[HotelSearchResponse])
async def search_hotels( location: str, date_from: date, date_to: date, db: AsyncSession = Depends( get_db ), current_user: User = Depends(get_current_user) ):

    if date_from >= date_to:
        raise HTTPException( status_code=400, detail= "The arrival date must be before the departure date" )

    return await search_hotels_by_availability( db, location, date_from, date_to )



@router.get ( "/{hotel_id}", response_model = HotelResponse )
async def read_hotel_by_id ( hotel_id: int, db: AsyncSession = Depends( get_db ), current_user: User = Depends(get_current_user) ):

    hotel = await get_hotel_by_id( db, hotel_id )

    if not hotel:
        raise HTTPException ( status_code=404, detail="Hotel not found" )

    return hotel

@router.post( "/create", response_model = HotelResponse )
async def create_hotell( hotel_in: HotelCreate, db: AsyncSession = Depends( get_db ), admin: User = Depends(get_current_admin) ):
    hotel = await create_hotel( db, hotel_in )
    return hotel


@router.patch("/{hotel_id}", response_model=HotelResponse)
async def patch_hotel(
    hotel_id: int,
    hotel_in: HotelUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Частичное обновление данных отеля"""
    return await update_hotel(db, hotel_id, hotel_in)

@router.delete("/{hotel_id}")
async def remove_hotel(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Удаление отеля по ID"""
    return await delete_hotel(db, hotel_id)

@router.get("/{hotel_id}/full", response_model=HotelWithRoomsResponse)
async def read_full_hotel_info(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #Возвращает всю информацию об отеле, включая список всех его комнат
    return await get_hotel_full_info(db, hotel_id)


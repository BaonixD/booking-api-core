from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.hotels import get_all_hotels, get_hotel_by_id, create_hotel
from app.schemas.hotel import HotelResponse, HotelListResponse, HotelCreate


router = APIRouter( prefix="/hotels", tags=["Hotels"] )

@router.get( "/", response_model= list[HotelListResponse] )
async def get_hotels( db: AsyncSession = Depends(get_db) ):
    return await get_all_hotels(db)

@router.get ( "/{hotel_id}", response_model = HotelResponse )
async def read_hotel_by_id ( hotel_id: int, db: AsyncSession = Depends( get_db ) ):

    hotel = await get_hotel_by_id( db, hotel_id )

    if not hotel:
        raise HTTPException ( status_code=404, detail="Hotel not found" )

    return hotel

@router.post( "/create", response_model = HotelResponse )
async def create_hotell( hotel_in: HotelCreate, db: AsyncSession = Depends( get_db ) ):
    hotel = await create_hotel( db, hotel_in )
    return hotel

from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_rout
from app.api.v1.endpoints.hotel import router as hotels_router
from app.api.v1.endpoints.room import router as rooms_router
from app.api.v1.endpoints.booking import router as bookings_router
from app.api.v1.endpoints.review import router as review_router
from app.models.User import User
from app.models.Hotel import Hotels
from app.models.Room import Rooms
from app.models.Booking import Bookings

app = FastAPI(title="Booking API")
app.include_router(auth_rout)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(review_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Booking API Core"}
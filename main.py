from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_rout
from app.models.User import User
from app.models.Hotel import Hotels
from app.models.Room import Rooms
from app.models.Booking import Bookings

app = FastAPI(title="Booking API")
app.include_router(auth_rout)

@app.get("/")
def read_root():
    return {"message": "Welcome to Booking API Core"}
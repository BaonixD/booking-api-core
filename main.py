from fastapi import FastAPI

app = FastAPI(title="Booking API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Booking API Core"}
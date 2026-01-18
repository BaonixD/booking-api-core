from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authorization"])

@router.post("/register", response_model=UserResponse)
async def register( user_in: UserCreate, db: AsyncSession = Depends(get_db) ):

    # чекаем не занят ли email
    user = await get_user_by_email(db, email=user_in.email) #await обязателен в ассинхронке

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await create_user(db, user=user_in)


@router.post("/login")
async def login( db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends() ):

    user = await get_user_by_email(db, email=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password ):

        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 3 Создаем токен (в sub кладем ID пользователя как строку)
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}

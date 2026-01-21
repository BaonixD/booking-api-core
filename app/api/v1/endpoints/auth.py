from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.TokenSchema import TokenResponse, TokenRefreshResponse, TokenRefreshRequest
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token, create_tokens, create_refresh_tokens, decode_token
from app.crud.token import add_refresh_token, rotate_refresh_token, get_token_from_db


router = APIRouter(prefix="/auth", tags=["Authorization"])

@router.post("/register", response_model=UserResponse)
async def register( user_in: UserCreate, db: AsyncSession = Depends(get_db) ):

    # чекаем не занят ли email
    user = await get_user_by_email(db, email=user_in.email) #await обязателен в ассинхронке

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await create_user(db, user=user_in)


@router.post( "/login", response_model= TokenResponse )
async def login ( db: AsyncSession = Depends(get_db),
                  form_data: OAuth2PasswordRequestForm = Depends()
                  ):
    # ищем юзера
    user = await get_user_by_email(db, email = form_data.username)

    # чекаем есть ли такой юзер
    if not user or not verify_password( form_data.password, user.hashed_password ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    # создаем токены
    tokens = create_tokens( user_id= user.id )

    # добавляем в БД
    await add_refresh_token( db, user.id, tokens["refresh_token"] )

    return tokens


@router.post( "/refresh", response_model=TokenRefreshResponse )
async def refresh( request: TokenRefreshRequest, db: AsyncSession = Depends(get_db) ):

    # декодтируем токен и проверяем, что это именно рефреш токен
    payload = decode_token( request.refresh_token, token_type="refresh" )
    user_id = payload.get("sub")

    # чекаем в БД есть ли такой токен
    db_token = await get_token_from_db( db, request.refresh_token )
    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token invalid or revoked")

    new_access_token = create_access_token(data={"sub": str(user_id)})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(
        request: TokenRefreshRequest,  # Используем твою схему
        db: AsyncSession = Depends(get_db)
):
    db_token = await get_token_from_db(db, request.refresh_token)

    # 2. Если нашли удаляем
    if db_token:
        await rotate_refresh_token(db, db_token)
        return {"detail": "Successfully logged out"}

    # 3. Если токена уже нет (или он неверный), все равно говорим "Ок" или кидаем ошибку
    raise HTTPException(status_code=400, detail="Token not found")
from passlib.context import CryptContext
import jwt
from app.core.config import settings
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# получаем пароль от пользователя, хэшируем и сравниваем с тем что есть в базе
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    # если указывается точное время токена то ставим его, если нет то дефолтную настройку ставим из сэттинга
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # обновляем время жизни токена
    to_encode.update({ "exp": expire, "type": "access" })
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_tokens( data: dict, expires_delta: Optional[timedelta] = None ) -> str:
    to_encode = data.copy()

# создается точно также как и аксес токен
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta( days=settings.REFRESH_TOKEN_EXPIRE_DAYS )

    to_encode.update({"exp": expire, "type": "refresh"})

    encode_jwt = jwt.encode( to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM )

    return encode_jwt

def create_tokens( user_id: int ) -> dict:

    access_token = create_access_token( data={"sub": str(user_id)} )
    refresh_token = create_refresh_tokens( data={"sub": str(user_id)} )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


from typing import Literal


def decode_token(
        token: str,
        token_type: Literal["access", "refresh"] = "access"
) -> dict:
    try:
        # Выбираем секрет в зависимости от того, что проверяем
        secret_key = (
            settings.REFRESH_SECRET_KEY
            if token_type == "refresh"
            else settings.SECRET_KEY
        )

        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])

        # Проверяем, что нам не подсунули refresh вместо access
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
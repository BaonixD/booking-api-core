from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.security import decode_token
from app.models.User import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
        session: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme) #передаем в функцию зашифрованный токен
) -> User:

    # Здесь decode_token либо вернет валидный payload,
    # либо сам выкинет HTTPException, и код ниже просто не выполнится.
    payload = decode_token(token)

    # Теперь мы на 100% уверены, что "sub" там есть, subject = субъект. primary key или id в базе данных
    # так как мы проверили это внутри decode_token.
    user_id = payload.get("sub")

    # ищем юзера в базе
    query = select(User).where(User.id == int(user_id) )
    result = await session.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


async def get_current_admin( current_user: User = Depends( get_current_user ) ) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough rights"
        )
    return current_user

async def get_user_by_email(session: AsyncSession, email: str):
    """Нужна для проверки при регистрации и для логина"""
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    return result.scalars().first()


async def create_user(session: AsyncSession, user: UserCreate):
    """Создание нового юзера с хешированием пароля"""
    hashed_pass = get_password_hash(user.password)

    # Создаем объект модели
    new_user = User(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        hashed_password=hashed_pass
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

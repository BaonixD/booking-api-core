from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from app.crud import review as crud_review
from app.crud.user import get_current_user  # Твоя готовая функция
from app.models.User import User  # Импорт модели юзера для аннотации типов

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewResponse)
async def create_my_review(
        review_in: ReviewCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)  # Сами берем юзера из токена
):
    # user_id берем из объекта current_user, который вернула твоя функция
    return await crud_review.create_review(db, review_in, user_id=current_user.id)


@router.get("/hotel/{hotel_id}", response_model=List[ReviewResponse])
async def get_hotel_reviews(
        hotel_id: int,
        db: AsyncSession = Depends(get_db)
):
    return await crud_review.get_hotel_review(db, hotel_id)


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_my_review(
        review_id: int,
        review_in: ReviewUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 1. Ищем отзыв
    db_review = await crud_review.get_review_by_id(db, review_id)

    # 2. Проверяем, существует ли он
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    # 3. ПРОВЕРКА: является ли текущий юзер автором этого отзыва
    if db_review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own reviews"
        )

    return await crud_review.update_review(db, review_in, review_id)


@router.delete("/{review_id}")
async def delete_my_review(
        review_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_review = await crud_review.get_review_by_id(db, review_id)

    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Проверка на владение перед удалением
    if db_review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own reviews"
        )

    await crud_review.delete_review(db, review_id)
    return {"detail": "Review deleted successfully"}
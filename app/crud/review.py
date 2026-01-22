from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.Review import Reviews
from app.schemas.review import ReviewCreate, ReviewUpdate

# create
async def create_review ( session: AsyncSession, review_in: ReviewCreate, user_id: int ):
    new_review = Reviews( **review_in.model_dump(), user_id=user_id )

    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review


# read
async def get_hotel_review ( session: AsyncSession, hotel_id: int ):

    query = select(Reviews).where( Reviews.hotel_id == hotel_id )
    res = await session.execute(query)
    return  res.scalars().all()

async def get_review_by_id ( session: AsyncSession, review_id: int ):

    query = select(Reviews).where( Reviews.id == review_id )
    res = await session.execute(query)
    return res.scalars().first()

# update
async def update_review ( session: AsyncSession, review_in: ReviewUpdate, review_id: int ):

    review = await get_review_by_id(session, review_id)

    if not review:
        return None

    update_data = review_in.model_dump( exclude_unset=True )

    for key, value in update_data.items():
        setattr( review, key, value )

    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review

# delete
async def delete_review ( session: AsyncSession, review_id: int ):

    review = await get_review_by_id(session, review_id)

    await session.delete(review)
    await session.commit()
    return {"message": "Review deleted successfully"}





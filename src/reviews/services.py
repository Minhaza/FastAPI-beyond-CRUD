from fastapi import HTTPException, status
from sqlmodel import desc, select
from src.db.models import Review
from src.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import UserService
from src.books.services import BookService

user_service = UserService()
book_service = BookService()

class ReviewService:
    async def add_review_to_book(self, user_email: str, book_id: str, review_data: ReviewCreateModel, session: AsyncSession):
        try:
            user = await user_service.get_user_by_email(user_email, session)
            book = await book_service.get_book_by_id(book_id, session)
            
            if not user:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
            if not book:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
            
            new_review_dict = review_data.model_dump()
            new_review = Review(**new_review_dict)
            
            new_review.user = user
            new_review.book = book
        
            session.add(new_review)
            await session.commit()    

            return new_review
        
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error adding new review")
        
    
    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        
        result = await session.exec(statement)
        return result.all()
    
    async def get_review_by_id(self, review_id: str, session: AsyncSession):
        statement = select(Review).where(Review.id == review_id)
        
        result = await session.exec(statement)
        return result.first()
    
    
    async def delete_review(self, review_id: str, session: AsyncSession):
        review = await self.get_review_by_id(review_id, session)
        
        if review is None:
            return None
        
        await session.delete(review)
        await session.commit()
        
        return {}

        
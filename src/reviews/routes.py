from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker, get_current_user
from src.db.main import get_session
from src.db.models import Review, User
from src.reviews.schemas import ReviewCreateModel, ReviewModel
from src.reviews.services import ReviewService


review_router = APIRouter()
review_service = ReviewService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

##GET
@review_router.get("/", response_model=List[Review], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_all_reviews(session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    reviews = await review_service.get_all_reviews(session)
    return reviews


@review_router.get("/{review_id}", response_model=ReviewModel, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_review_by_id(review_id: str, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    review = await review_service.get_review_by_id(review_id, session)
    
    if review is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Review not found")
    
    return review


##POST
@review_router.post("/book/{book_id}", status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_review(book_id: str, 
                        review_data: ReviewCreateModel, 
                        current_user: User = Depends(get_current_user), 
                        session: AsyncSession = Depends(get_session), 
                        token_details: dict = Depends(access_token_bearer)):
    
    new_review = await review_service.add_review_to_book(current_user.email, book_id, review_data, session)
    return new_review

##DELETE
@review_router.delete("/review/{review_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_review(review_id: str, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    review = await review_service.delete_review(review_id, session)
    
    if review is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Review not found")
    
    return {}
    
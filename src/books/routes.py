from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import TokenBearer
from src.books.models import Book
from .schemas import BookModel, BookUpdateModel, BookCreateModel
from .services import BookService
from src.db.main import get_session
# from .data import books

book_router = APIRouter()
book_service = BookService()
access_token_bearer = TokenBearer()

@book_router.get("/", status_code=status.HTTP_200_OK, response_model= List[Book])
async def get_all_books(session:AsyncSession = Depends(get_session), 
                        user_details = Depends(access_token_bearer)):
    print(user_details)
    
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=Book)
async def get_book_by_id(book_id: str, 
                         session:AsyncSession = Depends(get_session), 
                         user_details = Depends(access_token_bearer)) -> dict:
    
    book = await book_service.get_book_by_id(book_id, session)
    
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return book


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data: BookCreateModel, 
                      session:AsyncSession = Depends(get_session), 
                      user_details = Depends(access_token_bearer)) -> dict:
    
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.patch("/{book_id}", status_code=status.HTTP_200_OK, response_model=Book)
async def update_book_by_id(book_id: str, book_update_data: BookUpdateModel, 
                            session:AsyncSession = Depends(get_session), 
                            user_details = Depends(access_token_bearer)) -> dict:
    
    updated_book = await book_service.update_book_by_id(book_id, book_update_data, session)
            
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: str, 
                            session:AsyncSession = Depends(get_session), 
                            user_details = Depends(access_token_bearer)):
    
    book_delete = await book_service.delete_book_by_id(book_id, session)
    
    if book_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return {}
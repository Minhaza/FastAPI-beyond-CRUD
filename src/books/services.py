from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import desc, select
from .models import Book

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)
        
        return result.all() 
    
    async def get_book_by_id(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        
        result = await session.exec(statement)
        book = result.first()
        
        return book if book is not None else None
    
    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)

        new_book.published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")
        
        session.add(new_book)
        await session.commit()        

        return new_book
    
    async def update_book_by_id(self, book_id: str, book_data: BookUpdateModel, session: AsyncSession):
        book_update = await self.get_book_by_id(book_id, session)
        
        if book_update is None:
            return None
        
        update_data_dict = book_data.model_dump()
        
        for k, v in update_data_dict.items():
            setattr(book_update, k, v)
            
        await session.commit()
        
        return book_update        
    
    async def delete_book_by_id(self, book_id: str, session: AsyncSession):
        book_delete = await self.get_book_by_id(book_id, session)
        
        if book_delete is None:
            return None
        
        await session.delete(book_delete)
        await session.commit()
        
        return {}
            
    
    
    
    
    
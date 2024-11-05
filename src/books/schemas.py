from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class BookModel(BaseModel):
    id: UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    
class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "test",
                "author": "author_test",
                "publisher": "publisher_test",
                "published_date": "2024-05-11",
                "page_count": 100,
                "language": "English"
            }
        }
    }
    
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
from datetime import date, datetime
from re import L, U
import uuid
from fastapi.background import P
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, table
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "Books"
    
    id: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    def __repr__(self) -> str:
        return f"<Book {self.title}>"
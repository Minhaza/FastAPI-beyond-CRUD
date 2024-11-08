from datetime import date, datetime
from typing import List, Optional
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "Users"
    
    id: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    username: str
    password_hash: str = Field(exclude=True)
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    book: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    review: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    
class Book(SQLModel, table=True):
    __tablename__ = "Books"
    
    id: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="Users.id")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    user: Optional[User] = Relationship(back_populates="book")
    review: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})
    
    def __repr__(self) -> str:
        return f"<Book {self.title}>"



class Review(SQLModel, table=True):
    __tablename__ = "Reviews"
    
    id: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    review_text: str
    rating: int = Field(le=5)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="Users.id")
    book_id: Optional[uuid.UUID] = Field(default=None, foreign_key="Books.id")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    user: Optional[User] = Relationship(back_populates="review")
    book: Optional[Book] = Relationship(back_populates="review")
    
    def __repr__(self) -> str:
        return f"<Book {self.title}>"

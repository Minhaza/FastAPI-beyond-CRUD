from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, Field

from src.db.models import Book
from src.reviews.schemas import ReviewModel


class UserModel(BaseModel):
    id: uuid.UUID
    username: str
    password_hash: str = Field(exclude=True)
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    
class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@gmail.com",
                "password": "password",
            }
        }
    }


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe123@gmail.com",
                "password": "password"
            }
        }
    }
    
class UserBookModel(UserModel):
    book: List[Book]
    review: List[ReviewModel]
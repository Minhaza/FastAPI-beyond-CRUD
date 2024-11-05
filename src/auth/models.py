from datetime import datetime
import email
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "Users"
    
    id: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    username: str
    password_hash: str = Field(exclude=True)
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
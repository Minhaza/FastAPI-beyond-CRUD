from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreateModel, UserModel
from src.auth.services import UserService
from src.db.main import get_session


user_router = APIRouter()
user_service = UserService()

@user_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def sign_up(user_data: UserCreateModel, session:AsyncSession = Depends(get_session)) -> dict:
    is_exist = await user_service.is_user_exist(user_data.email, session)
    
    if is_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exist")
    
    new_user = await user_service.create_user(user_data, session)
    return new_user

@user_router.get("/{email}", status_code=status.HTTP_200_OK, response_model=UserModel)
async def get_user_by_email(email: str, session:AsyncSession = Depends(get_session)) -> dict:
    is_exist = await user_service.is_user_exist(email, session)
    
    if is_exist is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exist")
    
    user = await user_service.get_user_by_email(email, session)
    return user
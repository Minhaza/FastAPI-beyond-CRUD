from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker, get_current_user
from src.auth.models import User
from src.auth.schemas import UserBookModel, UserCreateModel, UserLoginModel, UserModel
from src.auth.services import UserService
from src.auth.utils import create_access_token, verify_password
from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist


auth_router = APIRouter()
user_service = UserService()
role_checker = Depends(RoleChecker(["admin"]))

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def sign_up(user_data: UserCreateModel, session:AsyncSession = Depends(get_session)) -> dict:
    is_exist = await user_service.is_user_exist(user_data.email, session)
    
    if is_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exist")
    
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.get("/get_user/{email}", status_code=status.HTTP_200_OK, response_model=UserModel, dependencies=[role_checker])
async def get_user_by_email(email: str, session:AsyncSession = Depends(get_session)) -> dict:
    is_exist = await user_service.is_user_exist(email, session)
    
    if is_exist is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    
    user = await user_service.get_user_by_email(email, session)
    return user

@auth_router.post("/login")
async def login(login_data: UserLoginModel, session:AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user_by_email(email, session)
    
    if user is not None:
        valid_password = verify_password(password, user.password_hash)

        if valid_password:
            
            user_data = {
                "email": user.email,
                "username": user.username,
                "id": str(user.id),
                "role": user.role
            }
                    
            access_token = create_access_token(
                user_data= user_data
            )
            
            refresh_token = create_access_token(
                user_data= user_data,
                refresh=True,
                expiry= timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            return JSONResponse(
                content= {
                    "message": "Login successfully",
                    "user": user_data,
                    "access_token": access_token,
                    "refresh_token": refresh_token                  
                }
            )
            
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Password is invalid")

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    
    jti = token_details['jti']
    
    await add_jti_to_blocklist(jti)
    
    return JSONResponse(
        content="Loggout successfully",
        status_code=status.HTTP_200_OK
    )
    
@auth_router.get("/me", response_model=UserBookModel)
async def get_current_user(user = Depends(get_current_user)):
    return user
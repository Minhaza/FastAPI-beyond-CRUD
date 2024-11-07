from datetime import datetime, timedelta
import logging
import uuid
import jwt
from passlib.context import CryptContext
from src.config import Config

pw_context = CryptContext(schemes=['bcrypt'])

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hash = pw_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return pw_context.verify(password, hash)
    
def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}
    
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    
    token = jwt.encode(
        payload=payload, 
        key=Config.JWT_SECRET, 
        algorithm=Config.JWT_ALGORITHM
    )
    
    return token
    
    
def decode_token(token: str) -> dict:
    
    try:
        token_data = jwt.decode(
            jwt=token, 
            key=Config.JWT_SECRET, 
            algorithms=Config.JWT_ALGORITHM
        )
        return token_data
    
    except jwt.PyJWTError as e:
        logging.error(e)
        return None
    
    
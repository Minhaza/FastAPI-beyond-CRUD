from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from src.db.redis import is_jti_in_blocklist

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials
        
        if not self.valid_token(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid or expired")
            
        token_data = decode_token(token)
        self.verify_token_data(token_data)
        
        if await is_jti_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid or revoked")
        
        return token_data
        

    
    def valid_token(self, token: str) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")
    
    
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")
    
    
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a refresh token")
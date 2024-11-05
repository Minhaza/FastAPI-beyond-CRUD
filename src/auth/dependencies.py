from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials
        
        if not self.valid_token(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid or expired")
            
        token_data = decode_token(token)
        
        if token_data is None or token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")

        return token_data
        

    
    def valid_token(self, token: str) -> bool:
        
        token_data = decode_token(token)
        
        return True if token_data is not None else False
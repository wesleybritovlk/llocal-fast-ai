from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.infra.setting import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        try:
            return await super().__call__(request)
        except HTTPException as e:
            if e.status_code == 403:
                raise HTTPException(status_code=401, detail=UNAUTHORIZED_MESSAGE)
            raise e

security = CustomHTTPBearer()

UNAUTHORIZED_MESSAGE = "Full authentication is required to access this resource"

def get_authorization_token(req: Request):
    if "Authorization" not in req.headers:
        raise HTTPException(status_code=401, detail=UNAUTHORIZED_MESSAGE)
    if not req.headers["Authorization"].startswith("Bearer"):
        raise HTTPException(status_code=401, detail=UNAUTHORIZED_MESSAGE)
    return req.headers.get("Authorization").split(" ")[1]

def get_authorization_payload(req: Request):
    token = get_authorization_token(req)
    return extract_token(token)

def extract_token(token: str):
    if not token:
        raise HTTPException(status_code=401, detail=UNAUTHORIZED_MESSAGE)
    try:
        payload = jwt.decode(token, Settings().JWT_SECRET_KEY, algorithms=[Settings().ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail=UNAUTHORIZED_MESSAGE)

async def validate_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
    token = credentials.credentials
    try:
        extract_token(token)
    except Exception: 
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_MESSAGE)

bearer_scheme = [Depends(validate_access)]
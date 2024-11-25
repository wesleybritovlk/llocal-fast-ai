from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from src.app.user.entity import UserEntity
from src.infra.setting import Settings
from src.infra.security import UNAUTHORIZED_MESSAGE, extract_token, pwd_context
from src.app.auth.dto import Request, Response
from src.app.user.service import UserService, get_user_service

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=Settings().GLOBAL_EXPIRATION)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Settings().JWT_SECRET_KEY, algorithm=Settings().ALGORITHM)
        return encoded_jwt

    def register(self, request: Request.Register) -> Response.Token:
        hashed_password = self.get_password_hash(request.password)
        request.password = hashed_password
        user = self.user_service.create(request)
        access_token = self.create_access_token(data=user)
        return Response.Token(
            access_token=access_token, 
            expires_in=Settings().GLOBAL_EXPIRATION * 60
        )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str):
        user = self.user_service.find_auth(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return {
            "sub": str(user.id),
            "name": user.email
        }

    def login(self, request: Request.Login):
        user = self.authenticate_user(request.email, request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        access_token = self.create_access_token(data=user)
        return Response.Token(
            access_token=access_token, 
            expires_in=Settings().GLOBAL_EXPIRATION * 60
        )

    def refresh_token(self, token: str): 
        try: 
            payload = extract_token(token) 
            user_id: str = payload["sub"]
            if user_id is None: 
                raise HTTPException(status_code=401, detail=AUTH_UNAUTHORIZED_MESSAGE) 
            user = self.user_service.find_one(user_id) 
            if not user: 
                raise HTTPException(status_code=401, detail=AUTH_UNAUTHORIZED_MESSAGE) 
        except JWTError: 
            raise HTTPException(status_code=401, detail="Invalid refresh token") 
        access_token = self.create_access_token(data={"sub": user_id}) 
        return Response.Token( 
            access_token=access_token, 
            expires_in=Settings().GLOBAL_EXPIRATION * 60 
        )

def get_auth_service(user_service = Depends(get_user_service)):
    return AuthService(user_service)

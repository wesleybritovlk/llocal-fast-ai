from fastapi import APIRouter, Depends, Request as Req
from src.infra.security import get_authorization_token, bearer_scheme
from src.main import bearer_scheme
from src.app.auth.service import AuthService, get_auth_service
from src.app.auth.dto import Response, Request
from src.core.common import  CommonResource, Message, MessageData, Data 

auth_router = APIRouter(prefix='/api/v1/auth', tags=['Auth'])

@auth_router.post("/register", status_code=201, 
    dependencies=None,
    description="Registeer a new user",
    response_model=MessageData[Response.Token], response_description="User registered successfully")
async def register(request: Request.Register, 
        service: AuthService = Depends(get_auth_service)):
    response = service.register(request)
    return CommonResource.to_message_data("User registered successfully", response)

@auth_router.post("/login",
    dependencies=None,
    description="Authenticate a user",
    response_model=MessageData[Response.Token], response_description="User authenticated successfully")
async def login(request: Request.Login, 
        service: AuthService = Depends(get_auth_service)):
    response = service.login(request)
    return CommonResource.to_message_data("User authenticated successfully", response)

@auth_router.get("/refresh_token", 
    dependencies=bearer_scheme,
    description="Refresh a user's token",
    response_model=MessageData[Response.Token], response_description="User token refreshed successfully")
async def refresh_token(request: Req, 
        service: AuthService = Depends(get_auth_service)):
    token = get_authorization_token(request)
    response = service.refresh_token(token)
    return CommonResource.to_message_data("User token refreshed successfully", response)
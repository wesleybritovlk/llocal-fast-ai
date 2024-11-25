from fastapi import APIRouter, Depends, Request as Req
from src.infra.security import get_authorization_payload
from src.app.user.dto import Response, Request
from src.core.common import  CommonResource, Message, MessageData, Data 
from src.app.user.service import UserService, get_user_service

users_router = APIRouter(prefix='/api/v1/users', tags=['Users'])

@users_router.get("/", description="Retrieve an user",
    response_model=Data[Response.User])
async def get(req: Req,  
        service: UserService = Depends(get_user_service)):
    user_id = get_authorization_payload(req)["sub"]
    response = service.find_one(user_id)
    return CommonResource.to_data(response)

@users_router.put("/", description="Update an user",
    response_model=MessageData[Response.User], response_description="User updated successfully")
async def update(req: Req, 
        request: Request.UserUpdate, 
        service: UserService = Depends(get_user_service)):
    user_id = get_authorization_payload(req)["sub"]
    response = service.update(user_id, request)
    return CommonResource.to_message_data("User updated successfully", response)


@users_router.delete("/", description="Delete an user",
    response_model=Message, response_description="User deleted successfully")
async def delete(req: Req,
        service: UserService = Depends(get_user_service)):
    user_id = get_authorization_payload(req)["sub"]
    service.delete(user_id)
    return CommonResource.to_message("User deleted successfully")

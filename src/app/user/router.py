from fastapi import APIRouter, Depends
from src.app.user.dto import Response, Request
from src.core.common import  CommonResource, Message, MessageData, Data 
from src.app.user.service import UserService, get_user_service

users_router = APIRouter(prefix='/api/v1/users', tags=['Users'])

@users_router.post("/", status_code=201, 
    description="Create a new user",
    response_model=MessageData[Response.User], response_description="User created successfully")
async def post(request: Request.UserCreate, 
        service: UserService = Depends(get_user_service)):
    response = service.create(request)
    return CommonResource.to_message_data("User created successfully", response)

@users_router.get("/{id}", 
    description="Retrieve an user",
    response_model=Data[Response.User])
async def get_one(id: str, 
        service: UserService = Depends(get_user_service)):
    response = service.find_one(id)
    return CommonResource.to_data(response)

@users_router.put("/{id}", 
    description="Update an user",
    response_model=MessageData[Response.User], response_description="User updated successfully")
async def update(id: str, request: Request.UserUpdate, 
        service: UserService = Depends(get_user_service)):
    response = service.update(id, request)
    return CommonResource.to_message_data("User updated successfully", response)


@users_router.delete("/{id}", 
    description="Delete an user",
    response_model=Message, response_description="User deleted successfully")
async def delete(id: str, 
        service: UserService = Depends(get_user_service)):
    service.delete(id)
    return CommonResource.to_message("User deleted successfully")

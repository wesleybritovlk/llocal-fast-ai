from fastapi import APIRouter, Depends
from src.app.property.dto import Response, Request
from src.core.common import  CommonResource, Message, MessageData, Data 
from src.app.property.service import PropertyService, get_property_service

properties_router = APIRouter(prefix='/api/v1/properties', tags=['Properties'])

@properties_router.post("/{user_id}", status_code=201, 
    description="Create a new property",
    response_model=MessageData[Response.Property], response_description="Property created successfully")
async def post(user_id: str, request: Request.PropertyCreate, 
        service: PropertyService = Depends(get_property_service)):
    response = service.create(user_id, request)
    return CommonResource.to_message_data("Property created successfully", response)

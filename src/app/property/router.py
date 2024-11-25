from fastapi import APIRouter, Depends, Path, Query, Request as Req
from src.infra.security import get_authorization_payload
from src.app.property.dto import Response, Request
from src.core.common import  CommonResource, Message, MessageData, Data, Page 
from src.app.property.service import PropertyService, get_property_service

properties_router = APIRouter(prefix='/api/v1/properties', tags=['Properties'])

@properties_router.post("/", status_code=201, 
    description="Create a new property",
    response_model=MessageData[Response.Property], response_description="Property created successfully")
async def post(req: Req, 
        request: Request.PropertyCreate, 
        service: PropertyService = Depends(get_property_service)):
    user_id = get_authorization_payload(req)["sub"]
    response = service.create(user_id, request)
    return CommonResource.to_message_data("Property created successfully", response)

@properties_router.get("/{id}", 
    description="Retrieve a property", 
    response_model=Data[Response.Property], 
    response_description="Property retrieved successfully")
async def get_one(req: Req,
        id: str = Path(..., description="Id of the property"), 
        service: PropertyService = Depends(get_property_service)):
    user_id = get_authorization_payload(req)["sub"]
    response = service.find_one(user_id, id)
    return CommonResource.to_data(response)


@properties_router.get("/", 
    description="Retrieve all properties", 
    response_model=Page[Response.PropertyShort], 
    response_description="Properties retrieved successfully")
async def get_all(req: Req,
        page: int = Query(0, description="Page number"), 
        size: int = Query(10, description="Page size"), 
        service: PropertyService = Depends(get_property_service)):
    user_id = get_authorization_payload(req)["sub"]
    response = service.find_all(user_id, page, size)
    return CommonResource.to_page(response)

@properties_router.put("/{id}", 
    description="Update a property", 
    response_model=MessageData[Response.Property], 
    response_description="Property updated successfully") 
async def put(req: Req,
            request: Request.PropertyUpdate, 
            id: str = Path(..., description="Id of the property"),
            service: PropertyService = Depends(get_property_service)): 
    user_id = get_authorization_payload(req)["sub"]
    response = service.update(user_id, id, request) 
    return CommonResource.to_message_data("Property updated successfully", response)


@properties_router.delete("/{id}", 
    description="Delete a property", 
    response_model=Message, 
    response_description="Property deleted successfully")
async def delete(req: Req,
            id: str = Path(..., description="Id of the property"), 
            service: PropertyService = Depends(get_property_service)):
    user_id = get_authorization_payload(req)["sub"]
    service.delete(user_id, id)
    return CommonResource.to_message("Property deleted successfully")
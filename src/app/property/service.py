from fastapi import Depends, HTTPException
from src.app.property.repository import PropertyRepository, get_property_repository
from src.app.property.entity import PropertyEntity
from src.app.property.dto import Response, Request
from decimal import Decimal
from src.infra.llm.service import LLMService
from src.infra.llm.template import PROPERTY_DESCRIPTION_TEMPLATE

class PropertyService:
    def __init__(self, repository: PropertyRepository):
        self.repository = repository
        self.llm_service = LLMService

    def generate_description(self, 
            property_data: Request.PropertyCreate | Request.PropertyUpdate):
        prompt_template = PROPERTY_DESCRIPTION_TEMPLATE
        context_data = property_data.dict()
        return self.llm_service.agent_invoke(prompt_template, context_data)

    def create(self, user_id: str, request: Request.PropertyCreate):
        description = self.generate_description(request)
        entity = PropertyEntity(
            property_type=request.property_type.name,
            description=description,
            price=request.price,
            area=request.area,
            bedrooms=request.bedrooms,
            bathrooms=request.bathrooms,
            parking=request.parking,
            address_full=request.address_full,
            coordinate_longitude=Decimal(0.0),
            coordinate_latitude=Decimal(0.0),
            user_id=user_id
        )
        entity = self.repository.create(entity)
        return Response.Property(
            id=str(entity.id),
            property_type=entity.property_type,
            description=entity.description,
            price=entity.price,
            area=entity.area,
            bedrooms=entity.bedrooms,
            bathrooms=entity.bathrooms,
            parking=entity.parking,
            address_full=entity.address_full,
            coordinate=Response.Coordinate(
                longitude=entity.coordinate_longitude,
                latitude=entity.coordinate_latitude
            )
        )

def get_property_service(repository = Depends(get_property_repository)):
    return PropertyService(repository)
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

    def exists_user(self, user_id: str):
        if not self.repository.exists_user_id(user_id):
            raise HTTPException(status_code=404, detail="User not found")

    def generate_description(self, 
            property_data: Request.PropertyCreate | Request.PropertyUpdate):
        prompt_template = PROPERTY_DESCRIPTION_TEMPLATE
        context_data = property_data.dict()
        return self.llm_service.agent_invoke(prompt_template, context_data)

    def create(self, user_id: str, request: Request.PropertyCreate):
        self.exists_user(user_id)
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

    def find_one(self, user_id: str, id: str):
        self.exists_user(user_id)
        entity = self.repository.find_by_id(id, user_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Property not found")
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
    
    def find_all(self, user_id: str, page: int, size: int):
        if page or size < 0:
            raise HTTPException(status_code=400, detail="Invalid page or size, cannot be negative")
        self.exists_user(user_id)
        entities = self.repository.find_all(user_id, page, size)
        properties = [
            Response.PropertyShort(
                id=str(entity.id),
                property_type=entity.property_type,
                price=entity.price,
                address_full=entity.address_full,
                bedrooms=entity.bedrooms,
                bathrooms=entity.bathrooms,
                area=entity.area,
                coordinate=Response.Coordinate(
                    longitude=entity.coordinate_longitude,
                    latitude=entity.coordinate_latitude
                )
            ) for entity in entities['data']
        ]
        entities.update({"data": properties})
        return entities

    def exists_property(self, id: str, user_id: str):
        if not self.repository.exists_property_by_user_id(id, user_id):
            raise HTTPException(status_code=404, detail="Property not found")

    def update(self, user_id: str, id: str, request: Request.PropertyUpdate):
        self.exists_user(user_id)
        self.exists_property(id, user_id)
        description = self.generate_description(request)
        entity = PropertyEntity(
            id=id,
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
        updated_rows = self.repository.update(entity)
        if updated_rows == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        return Response.Property(
            id=id,
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
            ))
    
    def delete(self, user_id: str, id: str):
        self.exists_user(user_id)
        deleted_rows = self.repository.delete_by_id(id, user_id)
        if deleted_rows == 0:
            raise HTTPException(status_code=404, detail="Property not found")

def get_property_service(repository = Depends(get_property_repository)):
    return PropertyService(repository)
from pydantic import BaseModel, Field
from decimal import Decimal
from src.app.property.entity import PropertyType

class Request:
    class PropertyCreate(BaseModel):
        property_type: PropertyType = Field(..., example="HOUSE", description="Type of the property (HOUSE or APARTMENT)")
        address_full: str = Field(..., example="123 Main St", description="Full address of the property")
        price: Decimal = Field(..., example=500000.00, description="Price of the property")
        area: int = Field(..., example=150, description="Total area in square meters")
        bedrooms: int = Field(..., example=3, description="Number of bedrooms")
        bathrooms: int = Field(..., example=2, description="Number of bathrooms")
        parking: int = Field(..., example=1, description="Number of parking spaces")

    class PropertyUpdate(BaseModel):
        property_type: PropertyType = Field(..., example="APARTMENT", description="Type of the property (HOUSE or APARTMENT)")
        address_full: str = Field(..., example="456 Elm St", description="Full address of the property")
        price: Decimal = Field(..., example=350000.00, description="Updated price of the property")
        area: int = Field(..., example=120, description="Updated area in square meters")
        bedrooms: int = Field(..., example=2, description="Updated number of bedrooms")
        bathrooms: int = Field(..., example=1, description="Updated number of bathrooms")
        parking: int = Field(..., example=1, description="Updated number of parking spaces")


class Response:
    class Coordinate(BaseModel):
        longitude: Decimal = Field(..., example=-50.12345, description="Longitude of the property location")
        latitude: Decimal = Field(..., example=-30.67890, description="Latitude of the property location")

    class Property(BaseModel):
        id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000", description="Unique identifier of the property")
        property_type: PropertyType = Field(..., example="HOUSE", description="Type of the property (HOUSE or APARTMENT)")
        address_full: str = Field(..., example="123 Main St", description="Full address of the property")
        price: Decimal = Field(..., example=500000.00, description="Price of the property")
        area: int = Field(..., example=150, description="Total area in square meters")
        bedrooms: int = Field(..., example=3, description="Number of bedrooms")
        bathrooms: int = Field(..., example=2, description="Number of bathrooms")
        parking: int = Field(..., example=1, description="Number of parking spaces")
        description: str = Field(..., example="A beautiful property", description="Description of the property")
        coordinate: "Response.Coordinate"

    class PropertyShort(BaseModel):
        id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000", description="Unique identifier of the property")
        property_type: PropertyType = Field(..., example="HOUSE", description="Type of the property (HOUSE or APARTMENT)")
        price: Decimal = Field(..., example=500000.00, description="Price of the property")
        address_full: str = Field(..., example="123 Main St", description="Full address of the property")
        bedrooms: int = Field(..., example=3, description="Number of bedrooms")
        bathrooms: int = Field(..., example=2, description="Number of bathrooms")
        area: int = Field(..., example=150, description="Total area in square meters")
        coordinate: "Response.Coordinate"

from sqlalchemy import Column, UUID, Text, Enum as SQLEnum, Numeric, SmallInteger, DateTime, Boolean, func, event
from sqlalchemy.schema import CreateSchema
from src.infra.database import Base
from uuid import uuid4
from datetime import datetime
from enum import Enum

class PropertyType(str, Enum):
    HOUSE = 'HOUSE'
    APARTMENT = 'APARTMENT'

class PropertyEntity(Base):
    __tablename__ = 'tb_property'
    __table_args__ = {"schema": "property"}
    
    id = Column(UUID, primary_key=True, default=lambda: uuid4())
    user_id = Column(UUID, nullable=False, index=True)
    description = Column(Text, nullable=False)
    property_type = Column(SQLEnum(PropertyType), nullable=False)
    price = Column(Numeric, nullable=False)
    area = Column(SmallInteger, nullable=False)
    bedrooms = Column(SmallInteger, nullable=False)
    bathrooms = Column(SmallInteger, nullable=False)
    parking = Column(SmallInteger, nullable=False)
    address_full = Column(Text, nullable=False, index=True)
    coordinate_longitude = Column(Numeric, nullable=False)
    coordinate_latitude = Column(Numeric, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

@event.listens_for(PropertyEntity.__table__, 'before_create')
def create_schema(target, connection, **kw):
    connection.execute(CreateSchema('property', if_not_exists=True))

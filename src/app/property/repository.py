from fastapi import Depends
from sqlalchemy.orm import Session
from src.infra.database import get_db
from src.app.property.entity import PropertyEntity

class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, entity: PropertyEntity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def find_all(self):
        return self.db.query(PropertyEntity).filter(
                PropertyEntity.is_deleted == False
            ).all()
    
    def find_by_id(self, id: str, user_id: str):
        return self.db.query(PropertyEntity).filter(
                PropertyEntity.is_deleted == False, PropertyEntity.id == id, PropertyEntity.user_id == user_id
            ).first()
    
    def update(self, entity: PropertyEntity):
        updated_rows = (self.db.query(PropertyEntity).filter(
                PropertyEntity.is_deleted == False, PropertyEntity.id == entity.id, PropertyEntity.user_id == entity.user_id
            ).update(
                {
                    PropertyEntity.description: entity.description,
                    PropertyEntity.price: entity.price,
                    PropertyEntity.area: entity.area,
                    PropertyEntity.bedrooms: entity.bedrooms,
                    PropertyEntity.bathrooms: entity.bathrooms,
                    PropertyEntity.parking: entity.parking,
                    PropertyEntity.address_full: entity.address_full,
                    PropertyEntity.coordinate_longitude: entity.coordinate_longitude,
                    PropertyEntity.coordinate_latitude: entity.coordinate_latitude
                },
                synchronize_session=False))
        if updated_rows:
            self.db.commit()
            return updated_rows
        return 0
    
    def delete_by_id(self, id: str, user_id: str):
        deleted_rows = (self.db.query(PropertyEntity).filter(
                PropertyEntity.is_deleted == False, PropertyEntity.id == id, PropertyEntity.user_id == user_id
        ).update(
                {PropertyEntity.is_deleted: True},
                synchronize_session=False))
        if deleted_rows:
            self.db.commit()
            return deleted_rows
        return 0

def get_property_repository(db = Depends(get_db)):
    return PropertyRepository(db)
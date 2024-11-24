from fastapi import Depends
from sqlalchemy.orm import Session
from src.infra.database import get_db
from src.app.property.entity import PropertyEntity
from src.app.user.entity import UserEntity

class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, entity: PropertyEntity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def exists_user_id(self, user_id: str):
        return self.db.query(
            self.db.query(UserEntity).filter(
                UserEntity.id == user_id, UserEntity.is_deleted == False
            ).exists()
        ).scalar() 

    def exists_property_by_user_id(self, property_id: str, user_id: str):
        return self.db.query(
            self.db.query(PropertyEntity).filter(
                PropertyEntity.id == property_id, PropertyEntity.user_id == user_id, PropertyEntity.is_deleted == False
            ).exists()
        ).scalar()

    def find_all(self, user_id: str, page: int, size: int): 
        offset = page * size 
        total_elements = self.db.query(PropertyEntity).filter( 
            PropertyEntity.is_deleted == False, PropertyEntity.user_id == user_id 
        ).count() 
        properties = self.db.query(PropertyEntity).filter( 
            PropertyEntity.is_deleted == False, PropertyEntity.user_id == user_id 
        ).offset(offset).limit(size).all() if size > 0 else []
        total_pages = (total_elements + size - 1) // size if size > 0 else size 
        current_page = page 
        is_first = current_page == 0 
        is_last = current_page == total_pages 
        return { 
            "data": properties, 
            "current_page": current_page, 
            "page_size": size, 
            "total_pages": total_pages, 
            "total_elements": total_elements, 
            "is_first": is_first, 
            "is_last": is_last, 
            "empty": not bool(properties) 
        }
    
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
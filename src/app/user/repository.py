from fastapi import Depends
from sqlalchemy.orm import Session
from src.infra.database import get_db
from src.app.user.entity import UserEntity

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, entity: UserEntity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def find_by_email(self, email: str):
        return self.db.query(UserEntity).filter(
            UserEntity.is_deleted == False, UserEntity.email == email
        ).first()
    
    def find_all(self):
        return self.db.query(UserEntity).filter(
                UserEntity.is_deleted == False
            ).all()
    
    def find_by_id(self, id: str):
        return self.db.query(UserEntity).filter(
            UserEntity.is_deleted == False, UserEntity.id == id
        ).first()
    
    def update(self, entity: UserEntity):
        updated_rows = (self.db.query(UserEntity).filter(
                UserEntity.is_deleted == False, UserEntity.id == entity.id
            ).update(
                {
                    UserEntity.fantasy_name: entity.fantasy_name,
                    UserEntity.cnpj: entity.cnpj,
                    UserEntity.email: entity.email
                },
                synchronize_session=False))
        if updated_rows:
            self.db.commit()
            return updated_rows
        return 0
    
    def delete_by_id(self, id: str):
        deleted_rows = (self.db.query(UserEntity).filter(
                UserEntity.is_deleted == False, UserEntity.id == id
            ).update(
                {UserEntity.is_deleted: True},
                synchronize_session=False))
        if deleted_rows:
            self.db.commit()
            return deleted_rows
        return 0

def get_user_repository(db = Depends(get_db)):
    return UserRepository(db)

from fastapi import Depends, HTTPException
from src.app.user.repository import UserRepository, get_user_repository
from src.app.user.entity import UserEntity
from src.app.auth.dto import Request as AuthRequest
from src.app.user.dto import Response, Request

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, request: AuthRequest.Register):
        entity = UserEntity(
            fantasy_name=request.fantasy_name,
            cnpj=request.cnpj,
            email=request.email,
            password=request.password
        )
        entity = self.repository.create(entity)
        return {
            "sub": str(entity.id),
            "name": entity.email
        }    

    def find_auth(self, username: str):
        return self.repository.find_by_email(username)

    def find_one(self, id: str):
        entity = self.repository.find_by_id(id)
        if not entity:
            raise HTTPException(status_code=404, detail="User not found")
        return Response.User(
            id=str(entity.id),
            fantasy_name=entity.fantasy_name,
            cnpj=entity.cnpj,
            email=entity.email
        )

    def update(self, id: str, request: Request.UserUpdate):
        entity = UserEntity(
            id=id,
            fantasy_name=request.fantasy_name,
            cnpj=request.cnpj,
            email=request.email
        )
        updated_rows = self.repository.update(entity)
        if updated_rows == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return Response.User(
            id=str(entity.id),
            fantasy_name=entity.fantasy_name,
            cnpj=entity.cnpj,
            email=entity.email
        )

    def delete(self, id: str):
        deleted_rows = self.repository.delete_by_id(id)
        if deleted_rows == 0:
            raise HTTPException(status_code=404, detail="User not found")

def get_user_service(repository = Depends(get_user_repository)):
    return UserService(repository)

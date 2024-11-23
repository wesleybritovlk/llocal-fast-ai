# main.py
from fastapi import FastAPI

app = FastAPI()

def entity_manager():
    from src.infra.database import Base, engine
    from src.app.user.entity import UserEntity
    from src.app.property.entity import PropertyEntity
    Base.metadata.create_all(bind=engine)

def router_manager():
    from src.app.user.router import users_router
    from src.app.property.router import properties_router
    app.include_router(users_router)
    app.include_router(properties_router)

entity_manager()
router_manager()



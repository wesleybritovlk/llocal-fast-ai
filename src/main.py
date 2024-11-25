from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.infra.security import validate_access, bearer_scheme

app = FastAPI(
    title="LLocal Fast AI",
    description="Simple API to register properties with AI",
    contact={
        "name": "Wesley Brito VLK",
        "url": "https://github.com/wesleybritovlk/llocal-fast-ai/issues"
    },
    version="0.1.0"
)

def entity_manager():
    from src.infra.database import Base, engine
    from src.app.user.entity import UserEntity
    from src.app.property.entity import PropertyEntity
    Base.metadata.create_all(bind=engine)

def router_manager():
    from src.app.auth.router import auth_router
    from src.app.user.router import users_router
    from src.app.property.router import properties_router
    app.include_router(auth_router)
    app.include_router(users_router, dependencies=bearer_scheme)
    app.include_router(properties_router, dependencies=bearer_scheme)

entity_manager()
router_manager()

@app.get("/", include_in_schema=False) 
def read_root(): 
    return RedirectResponse(url="/docs") 
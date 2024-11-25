from sqlalchemy import Column, UUID, String, DateTime, Boolean, func, event
from sqlalchemy.schema import CreateSchema
from uuid import uuid4
from src.infra.database import Base, engine

class UserEntity(Base):
    __tablename__ = "tb_user"
    __table_args__ = {"schema": "user"}

    id = Column(UUID, primary_key=True, default=lambda: uuid4())
    fantasy_name = Column(String, nullable=False)
    cnpj = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

@event.listens_for(UserEntity.__table__, 'before_create')
def create_schema(target, connection, **kw):
    connection.execute(CreateSchema('user', if_not_exists=True))

from pydantic import BaseModel, Field

class Request:
    class UserUpdate(BaseModel):
        fantasy_name: str = Field(..., example="Tech Solutions Ltda", description="Name of the company")
        cnpj: str = Field(..., example="12.345.678/0001-90", description="CNPJ of the company")
        email: str = Field(..., example="contact@techsolutions.com", description="Email of the company")

class Response:
    class User(BaseModel):
        fantasy_name: str = Field(..., example="Tech Solutions Ltda", description="Name of the company")
        cnpj: str = Field(..., example="12.345.678/0001-90", description="CNPJ of the company")
        email: str = Field(..., example="contact@techsolutions.com", description="Email of the company")

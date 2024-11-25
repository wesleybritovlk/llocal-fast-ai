from pydantic import BaseModel, Field
from typing import Optional

class Response:
    class Token(BaseModel):
        access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", description="JWT Access Token")
        token_type: str = "Bearer"
        expires_in: int = Field(..., example=3600, description="Expiration time in seconds")

class Request:
    class Register(BaseModel):
        fantasy_name: str = Field(..., example="Tech Solutions Ltda", description="Name of the company")
        cnpj: str = Field(..., example="12.345.678/0001-90", description="CNPJ of the company")
        email: str = Field(..., example="contact@techsolutions.com", description="Email of the company")
        password: str = Field(..., example="securepassword123", description="Password for the company account")

    class Login(BaseModel):
        email: str = Field(..., example="contact@techsolutions.com", description="Email of the company")
        password: str = Field(..., example="securepassword123", description="Password for the company account")

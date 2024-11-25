from typing import TypeVar, Generic, List
from pydantic import BaseModel, Field

T = TypeVar('T')

class Message(BaseModel):
    message: str = Field(..., example="Message in response description")

class MessageData(BaseModel, Generic[T]):
    message: str = Field(..., example="Message in response description")
    data: T

class Data(BaseModel, Generic[T]):
    data: T

class Page(BaseModel, Generic[T]):
    data: List[T]
    current_page: int
    page_size: int
    total_pages: int
    total_elements: int
    is_first: bool
    is_last: bool
    empty: bool

class CommonResource:
    @staticmethod
    def to_message(message: str) -> Message:
        return Message(message=message)

    @staticmethod
    def to_message_data(message: str, data: T) -> MessageData[T]:
        return MessageData(message=message, data=data)

    @staticmethod
    def to_data(data: T) -> Data[T]:
        return Data(data=data)

    @staticmethod
    def to_page(page_data: dict) -> Page[T]: 
        return Page( 
            data=page_data["data"], 
            current_page=page_data["current_page"], 
            page_size=page_data["page_size"], 
            total_pages=page_data["total_pages"], 
            total_elements=page_data["total_elements"], 
            is_first=page_data["is_first"], 
            is_last=page_data["is_last"], 
            empty=page_data["empty"] 
        )

from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar('T')

class Message(BaseModel):
    message: str

class MessageData(BaseModel, Generic[T]):
    message: str
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
    def to_page(page) -> Page[T]:
        return Page(
            data=page.data, 
            current_page=page.current_page, 
            page_size=page.page_size, 
            total_pages=page.total_pages, 
            total_elements=page.total_elements, 
            is_first=page.is_first, 
            is_last=page.is_last, 
            empty=page.empty
        )

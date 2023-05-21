from pydantic import BaseModel
from typing import List, Optional
from fastapi import Form


# class Item(BaseModel):
#     Item: str
#     status: str


class Todo(BaseModel):
    id: Optional[int]
    item: str
    
    @classmethod
    def as_form(
        cls,
        item: str = Form(...)
    ):
        return cls(item=item)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "item": "Example shema!"
            }
        }
# json스키마를 올바르게 생성하기 위해 사용자가 입력해야 할 데이터의 샘플을 설정할 수 있다. 


# update라우터의 요청 바디용 모델
class TodoItem(BaseModel):
    item: str

    class Config:
        schema_extra = {
            "example": {
                "item": "read the next chapter of the book." 
            }
        }


class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {
                        "item": "example schema 1!"
                    },
                    {
                        "item": "example schema 2!"
                    }
                ]
            }
        }
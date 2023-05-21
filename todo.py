# api라우터 클래스를 fastapi패키지에서 임포트 한 후 apirouter() 인스턴스를 만듬
from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []


@todo_router.post("/todo", status_code=201)  # todo_list에 todo를 추가하는 post메서드, 응답 코드 변경
async def add_todo(todo: Todo) -> dict:  # 요청 바디를 딕셔너리로 받는다
    todo_list.append(todo)  # 필요한 요청 바디 구조를 모델로 만들어서 요청 바디의 유형에 할당하면 모델에 정의된 데이터 필드만 처리함
    return {
        "message": "todo added successfully."
    }


@todo_router.get("/todo", response_model=TodoItems)  # 모든 todo아이템을 todo_list에서 조회하는 get메서드
async def retrieve_todos() -> dict:
    return {
        "todos": todo_list
    }


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="the id of the todo to retrieve.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="todo with supplied id doesn't exist",
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="the id of the todo to be update")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "Todo updated successfully"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="todo with supplied id doesn't exist",
    )


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": "todo deleted successfully."
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="todo with supplied id doesn't exist",
    )


@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "Todos deleted successfully"
    }
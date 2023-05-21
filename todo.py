# api라우터 클래스를 fastapi패키지에서 임포트 한 후 apirouter() 인스턴스를 만듬
from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []

templates = Jinja2Templates(directory="templates/")


@todo_router.post("/todo")  # todo_list에 todo를 추가하는 post메서드, 응답 코드 변경
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):  # 요청 바디를 딕셔너리로 받는다
    todo.id = len(todo_list) + 1
    todo_list.append(todo)  # 필요한 요청 바디 구조를 모델로 만들어서 요청 바디의 유형에 할당하면 모델에 정의된 데이터 필드만 처리함
    return templates.TemplateResponse("todo.html", {
            "request": request,
            "todos": todo_list
    })
# post메서드는 의존성을 사용하여 입력 값 전달

@todo_router.get("/todo", response_model=TodoItems)  # 모든 todo아이템을 todo_list에서 조회하는 get메서드
async def retrieve_todos(request: Request):
    return templates.TemplateResponse("todo.html", {
       "request": request,
       "todos": todo_list
    })
# jinja가 template폴더를 참조해서 그 안에 있는 특정 템플릿을 사용하도록 지정한다.   
# 템플릿은 templates.TemplateResponse() 메서드를 통해 전달됨


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(request: Request, todo_id: int = Path(..., title="the id of the todo to retrieve.")):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse("todo.html", {
                "request": request,
                "todo": todo
            })
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
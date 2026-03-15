from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from database.database import db,todos_collection,users_collection
from models import TodoCreate, TodoUpdate, TodoResponse
# from models import TodoCreate, TodoUpdate, TodoResponse,Todo
from auth import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])


def validate_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID format"
        )


# @router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
# def create_todo(
#     todo: Todo,
#     current_user: dict = Depends(get_current_user)
# ):
#     try:
#         print("todo_data",current_user,todo, current_user["_id"], todo.title, todo.description, datetime.now())
#         todo_doc = {
#             "user_id": current_user["_id"],
#             "title": todo.title if todo.title else None,
#             "description": todo.description if todo.description else None,
#             "completed": False,
#             "created_at": datetime.now()
#         }
#         todo_data = Todo(**todo_doc)
        
#         result = db.Todo.CollectionName.todo.insert_one(todo_data.model_dump(exclude=None))

#         return {
#             "id": str(result.inserted_id),
#             "title": todo.title,
#             "description": todo.description,
#             "completed": False,
#             "created_at": todo_doc["created_at"]
#         }

#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to create todo"
#         )
@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    current_user: dict = Depends(get_current_user)
):
    try:
        todo_doc = {
            "user_id": current_user["_id"],
            "title": todo.title,
            "description": todo.description,
            "completed": False,
            "created_at": datetime.utcnow()
        }

        result = todos_collection.insert_one(todo_doc)

        return {
            "id": str(result.inserted_id),
            "title": todo.title,
            "description": todo.description,
            "completed": False,
            "created_at": todo_doc["created_at"]
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create todo"
        )



@router.get("/", response_model=list[TodoResponse])
def get_todos(current_user: dict = Depends(get_current_user)):
    try:
        todos = []

        for todo in todos_collection.find({"user_id": current_user["_id"]}):
            todos.append({
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "completed": todo["completed"],
                "created_at": todo["created_at"]
            })

        return todos

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch todos"
        )

@router.put("/{todo_id}")
def update_todo(
    todo_id: str,
    todo: TodoUpdate,
    current_user: dict = Depends(get_current_user)
):
    obj_id = validate_object_id(todo_id)

    update_data = todo.model_dump()

    try:
        result = todos_collection.update_one(
            {"_id": obj_id, "user_id": current_user["_id"]},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not authorized"
            )

        return {"message": "Todo updated successfully"}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update todo"
        )


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: str,
    current_user: dict = Depends(get_current_user)
):
    obj_id = validate_object_id(todo_id)

    try:
        result = todos_collection.delete_one({
            "_id": obj_id,
            "user_id": current_user["_id"]
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not authorized"
            )

        return {"message": "Todo deleted successfully"}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete todo"
        )

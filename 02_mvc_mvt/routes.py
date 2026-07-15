
from fastapi import APIRouter, HTTPException
import services
from schemas import Task, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def get_tasks():
    return services.list_tasks()

@router.post("", response_model=Task, status_code=201)
def post_task(body: TaskCreate):
    return services.create_task(body)

@router.post("/{task_id}/complete", response_model=Task)
def post_complete(task_id: int):
    try:
        return services.complete_task(task_id)
    except services.NotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

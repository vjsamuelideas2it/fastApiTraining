from schemas import Task, TaskCreate

_store: dict[int, Task] = {}
_next = 1


class NotFoundError(Exception):
    pass


def list_tasks() -> list[Task]:
    return list(_store.values())


def create_task(data: TaskCreate) -> Task:
    global _next
    task = Task(id=_next, **data.model_dump())
    _store[_next] = task
    _next += 1
    return task


def complete_task(task_id: int) -> Task:
    if task_id not in _store:
        raise NotFoundError(f"task {task_id}")
    t = _store[task_id]
    updated = t.model_copy(update={"done": True})
    _store[task_id] = updated
    return updated

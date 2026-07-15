from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["users"])

_dummy_users = {
    1: "Alice",
    2: "Bob",
    3: "Charlie"
}


@router.get("")
def list_users():
    return _dummy_users


@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id not in _dummy_users:
        raise HTTPException(status_code=404, detail="User not found")
    return _dummy_users[user_id]
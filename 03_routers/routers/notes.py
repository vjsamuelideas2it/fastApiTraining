# Notes router — another feature module, separate from users.

from fastapi import APIRouter

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("")
def list_notes():
    return [{"id": 1, "body": "Note 1"}]


@router.post("")
def create_note(body: dict):
    return {"saved": body}

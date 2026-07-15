import hashlib
import secrets
from typing import Callable

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI(title="06 Roles & Permissions")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

ROLE_PERMS: dict[str, set[str]] = {
    "admin": {"notes:read", "notes:write", "notes:delete", "users:read"},
    "editor": {"notes:read", "notes:write"},
    "viewer": {"notes:read"},
}

USERS = {
    "root": {"username": "root", "password": _hash("rootpass"), "roles": ["admin"]},
    "ed": {"username": "ed", "password": _hash("editpass"), "roles": ["editor"]},
    "vie": {"username": "vie", "password": _hash("viewpass"), "roles": ["viewer"]},
}

TOKENS: dict[str, str] = {}
NOTES: list[dict] = [{"id": 1, "body": "readable by all roles"}]
_next_note = 2


class User(BaseModel):
    username: str
    roles: list[str]
    permissions: set[str]


def perms_for(roles: list[str]) -> set[str]:
    out: set[str] = set()
    for r in roles:
        out |= ROLE_PERMS.get(r, set())
    return out


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form.username)
    if not user or not secrets.compare_digest(user["password"], _hash(form.password)):
        raise HTTPException(status_code=401, detail="bad credentials")
    token = secrets.token_urlsafe(16)
    TOKENS[token] = form.username
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Step 1 — Authentication: who is this? (401 if unknown)
    username = TOKENS.get(token)
    if not username or username not in USERS:
        raise HTTPException(status_code=401, detail="invalid token")
    raw = USERS[username]
    return User(
        username=raw["username"],
        roles=raw["roles"],
        permissions=perms_for(raw["roles"]),
    )


def require_perm(permission: str) -> Callable:
    def checker(user: User = Depends(get_current_user)) -> User:
        if permission not in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"missing permission: {permission}",
            )
        return user
    return checker


@app.get("/me")
def me(user: User = Depends(get_current_user)):
    # GET /me — any logged-in user can see their own roles and permissions.
    return {
        "username": user.username,
        "roles": user.roles,
        "permissions": sorted(user.permissions),
    }


@app.get("/notes")
def list_notes(_: User = Depends(require_perm("notes:read"))):
    return NOTES


@app.post("/notes", status_code=201)
def add_note(body: dict, user: User = Depends(require_perm("notes:write"))):
    global _next_note
    note = {"id": _next_note, "body": body.get("body", ""), "by": user.username}
    NOTES.append(note)
    _next_note += 1
    return note


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, _: User = Depends(require_perm("notes:delete"))):
    idx = next((i for i, n in enumerate(NOTES) if n["id"] == note_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="not found")
    NOTES.pop(idx)

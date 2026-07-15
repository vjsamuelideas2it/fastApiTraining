
import hashlib
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI(title="05 Auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "ada": {
        "username": "ada",
        "full_name": "Ada Lovelace",
        "hashed_password": _hash("analytical"),
    }
}

TOKENS: dict[str, str] = {}


class UserPublic(BaseModel):
    username: str
    full_name: str


def authenticate(username: str, password: str) -> dict | None:
    user = USERS.get(username)
    if not user:
        return None
    if not secrets.compare_digest(user["hashed_password"], _hash(password)):
        return None
    return user


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = secrets.token_urlsafe(16)
    TOKENS[token] = user["username"]
    return {"access_token": token, "token_type": "bearer"}


def current_user(token: str = Depends(oauth2_scheme)) -> UserPublic:
    username = TOKENS.get(token)
    if not username or username not in USERS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    u = USERS[username]
    return UserPublic(username=u["username"], full_name=u["full_name"])


@app.get("/public")
def public():
    return {"msg": "no auth required"}


@app.get("/me", response_model=UserPublic)
def me(user: UserPublic = Depends(current_user)):
    return user

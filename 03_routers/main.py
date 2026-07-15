from fastapi import FastAPI

from routers import health, notes, users

app = FastAPI()

app.include_router(health.router)
app.include_router(users.router)
app.include_router(notes.router)

import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="04 Middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def timing_and_request_id(request: Request, call_next):
    rid = str(uuid.uuid4())[:8]
    started = time.perf_counter()
    print(f"→ [{rid}] {request.method} {request.url.path}")

    response = await call_next(request)

    ms = (time.perf_counter() - started) * 1000
    response.headers["X-Request-Id"] = rid
    response.headers["X-Process-Ms"] = f"{ms:.1f}"
    print(f"← [{rid}] {response.status_code} ({ms:.1f}ms)")
    return response

@app.middleware("http")
async def block_evil_ua(request: Request, call_next):
    ua = request.headers.get("user-agent", "")
    if "EvilBot" in ua:
        return JSONResponse({"detail": "bots not welcome"}, status_code=403)
    return await call_next(request)


# --- Routes (these run INSIDE the middleware onion) ---


@app.get("/")
def root():
    # GET / — check response headers in /docs for X-Request-Id and X-Process-Ms.
    return {"msg": "check response headers + terminal logs"}


@app.get("/slow")
async def slow():
    # GET /slow — fake slow endpoint so you can see timing in logs (~300ms).
    import asyncio

    await asyncio.sleep(0.3)
    return {"msg": "artificial delay"}

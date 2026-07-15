# FastAPI — One-Night Crash Course

React → FastAPI mental map, then six labs. Do them **in order**. Each lab: read `CONCEPT.md`, run the code, answer the probe questions out loud (as if in an interview).

```bash
source .venv/bin/activate
# from any lab folder:
uvicorn main:app --reload
# docs: http://127.0.0.1:8000/docs
```

| # | Topic | Folder | React analogy |
|---|--------|--------|---------------|
| 1 | REST basics | `01_rest/` | Fetching/posting to API endpoints you already consume |
| 2 | MVC / MVT | `02_mvc_mvt/` | Component splits: UI vs logic vs data |
| 3 | Routers | `03_routers/` | React Router — path → handler modules |
| 4 | Middleware | `04_middleware/` | Axios interceptors / Express middleware |
| 5 | Auth | `05_auth/` | JWT in headers / protected routes |
| 6 | Roles & perms | `06_roles/` | RBAC guards on routes/components |

No giant app. Each file is short on purpose — you must be able to whiteboard it.

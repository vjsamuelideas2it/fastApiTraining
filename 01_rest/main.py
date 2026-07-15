
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

db: dict[int, dict] = {}
_next_id = 1

class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=50) 
    price: float = Field(gt=0)


class ItemOut(ItemIn):
    id: int


@app.get("/")
def root():
    return {"hint": "open /docs"}

@app.get("/items", response_model=list[ItemOut])
def list_items(q: str | None = None):
    items = list(db.values())
    if q:
        items = [i for i in items if q.lower() in i["name"].lower()]
    return items


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]


@app.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(body: ItemIn):
    global _next_id
    item = {"id": _next_id, **body.model_dump()}
    db[_next_id] = item
    _next_id += 1
    return item


@app.patch("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, body: ItemIn):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = {"id": item_id, **body.model_dump()}
    return db[item_id]


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]

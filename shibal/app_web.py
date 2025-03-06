from fastapi import FastAPI

from app.routers.users import router as router_users

app = FastAPI()

app.include_router(router_users)


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/")
async def read_items(q: str | None = None):
    if q:
        return {
            "items": [
                {"item_id": 1, "name": "Item 1"},
                {"item_id": 2, "name": "Item 2"},
            ]
        }
    else:
        return {"items": [{"item_id": 1, "name": "Item 1"}]}

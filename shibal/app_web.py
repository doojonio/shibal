from fastapi import FastAPI

from app.routers.users import router as router_users

app = FastAPI()

app.include_router(router_users)


@app.get("/")
async def root():
    return {"Hello": "World"}

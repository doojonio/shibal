from fastapi import FastAPI

from app.routers.api import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def root():
    return {"Hello": "World"}

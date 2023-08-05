from fastapi import FastAPI

from app.api.v1 import user

app = FastAPI()

app.include_router(user.router)


@app.get("/", tags=["status"])
async def health_check():
    return "API is working"

from fastapi import FastAPI

from app.api.v1 import post, user

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)


@app.get("/", tags=["status"])
async def health_check():
    return "API is working"

from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["status"])
async def health_check():
    return "API is working"

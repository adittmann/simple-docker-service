import uvicorn
from fastapi import FastAPI

from app.api import images

app = FastAPI()

app.include_router(images.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

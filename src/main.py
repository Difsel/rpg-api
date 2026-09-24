from fastapi import FastAPI

from src.routers.registration import router as registerRouter
from src.routers.user import router as userRouter

app = FastAPI()

app.include_router(registerRouter)
app.include_router(userRouter)

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

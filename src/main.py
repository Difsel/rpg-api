from fastapi import FastAPI

from src.routers.authRouter import router as AuthRouter
from src.routers.userRouter import router as UserRouter

app = FastAPI()

app.include_router(AuthRouter)
app.include_router(UserRouter)

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

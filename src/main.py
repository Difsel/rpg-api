from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.redis.redis import create_redis
from src.routers.authRouter import router as AuthRouter
from src.routers.userRouter import router as UserRouter
from src.routers.characterRouter import router as CharacterRouter
from src.exceptions.handlers import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
	app.state.redis = create_redis()

	yield

	await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(CharacterRouter)

@app.get("/")
async def root():
	return {"message": "Backend is running!"}
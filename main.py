from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from router import router as tasks_touter


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    print("База готова")
    yield
    print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(router=tasks_touter)

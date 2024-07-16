from fastapi import FastAPI
from contextlib import asynccontextmanager
from router import router as tasks_touter
from database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    print("База готова")
    yield
    print("База очищена")

app = FastAPI(lifespan=lifespan)
app.include_router(router=tasks_touter)


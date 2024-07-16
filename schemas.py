from pydantic import BaseModel, validator
from typing import Optional


class STaskADD(BaseModel):
    name: str
    description: Optional[str] = None

    @validator('name')
    def name_must_be_positive(cls, value):
        if len(value) < 1:
            raise ValueError('Имя должно быть длиннее 0')
        return value


class STask(STaskADD):
    id: int


class STaskId(BaseModel):
    ok: bool = True
    task_id: int

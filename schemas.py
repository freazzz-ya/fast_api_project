from typing import Optional

from pydantic import BaseModel, ConfigDict, validator


class STaskGetByIdOne(BaseModel):
    id: int


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

    model_config = ConfigDict(from_attributes=True)


class STaskId(BaseModel):
    ok: bool = True
    task_id: int


class STaskDel(BaseModel):
    task_id: int

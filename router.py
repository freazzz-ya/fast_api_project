from typing import Annotated, Optional, Union, Dict
from fastapi import Depends
from fastapi import APIRouter

from schemas import STaskADD, STask, STaskId, STaskDel, STaskGetByIdOne
from repository import TaskRepository

router = APIRouter(
    prefix='/tasks',
    tags=['Таски'],
)


@router.post('')
async def add_tasks(
    task: Annotated[STaskADD, Depends()],
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {
        'ok': True, 'task_id': task_id
    }


@router.get('')
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks


@router.get('/{task_id}')
async def get_task_by_id(
    task: Annotated[STaskGetByIdOne, Depends()]
) -> Union[STaskId, None]:
    data = STaskGetByIdOne(id=task.id)
    task_schema = await TaskRepository.get_task_by_id(data)
    if task_schema:
        return STaskId(task_id=task_schema.id)
    else:
        # Обработка случая, когда объект не найден
        return None


@router.patch('')
async def patch_tasks(
    task: Annotated[STaskADD, Depends()],
) -> STaskId:
    pass


@router.delete('')
async def delete_tasks(
    task: Annotated[STaskGetByIdOne, Depends()]
):
    data = STaskGetByIdOne(id=task.id)
    task_schema = await TaskRepository.delete_task_by_id(data)
    print(task_schema)
    if task_schema:
        return {'True': 'delete'}
    else:
        # Обработка случая, когда объект не найден
        return {'error': 'error'}

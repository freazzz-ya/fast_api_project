from typing import Annotated, Union, Dict
from fastapi import Depends
from fastapi import APIRouter

from schemas import STaskADD, STask, STaskId, STaskGetByIdOne
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
) -> Union[STaskId, Dict]:
    data = STaskGetByIdOne(id=task.id)
    task_schema = await TaskRepository.get_task_by_id(data)
    if task_schema:
        return STaskId(task_id=task_schema.id)
    else:
        # Обработка случая, когда объект не найден
        return {
            'error': 'такого объекта нет'
        }


@router.delete('')
async def delete_tasks(
    task: Annotated[STaskGetByIdOne, Depends()]
) -> Union[STaskId, Dict]:
    data = STaskGetByIdOne(id=task.id)
    task = await TaskRepository.delete_task_by_id(data)
    if task:
        return {
            'ok': task.id
        }
    return {
        'error': 'такого объекта нет'
    }


@router.patch('')
async def patch_tasks(
    task: Annotated[STask, Depends()],
) -> Union[STask, dict]:
    task = await TaskRepository.update_task(task)
    if task:
        return task
    return {
        'error': 'такого объекта нет'
    }

from typing import Optional, Union

from sqlalchemy import delete, select

from database import TaskOrm, new_session
from schemas import STask, STaskADD, STaskGetByIdOne


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskADD):
        async with new_session() as session:
            #  перевод в словарь
            task_dict = data.model_dump()
            task = TaskOrm(**task_dict)
            session.add(task)
            #  до коммита обновляет таск что присваивает ему id
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            # перевод к pydantic
            task_schemas = [
                STask.model_validate(task_model)
                for task_model in task_models
            ]
            return task_schemas

    @classmethod
    async def get_task_by_id(cls, data: STaskGetByIdOne) -> Optional[STask]:
        async with new_session() as session:
            query = select(TaskOrm).where(TaskOrm.id == data.id)
            result = await session.execute(query)
            task_model = result.scalars().first()
            if task_model:
                task_schema = STask.model_validate(task_model)
                return task_schema
            else:
                return None

    @classmethod
    async def delete_task_by_id(cls, data: STaskGetByIdOne) -> bool:
        async with new_session() as session:
            # Check if the task exists before attempting to delete
            query = select(TaskOrm).where(TaskOrm.id == data.id)
            result = await session.execute(query)
            task_model = result.scalars().first()

            if task_model:
                # Delete the task if it exists
                query = delete(TaskOrm).where(TaskOrm.id == data.id)
                await session.execute(query)
                await session.commit()
                return task_model  # Return True if deletion was successful
            else:
                return False  # Return False if the task doesn't exist

    @classmethod
    async def update_task(cls, data: STask) -> Union[STask, None]:
        async with new_session() as session:
            task = await session.get(TaskOrm, data.id)
            if not task:
                return False  # или raise exception
            #  обновляем атрибуты таска
            for key, value in data.model_dump().items():
                if key != 'id':
                    setattr(task, key, value)
            #  сохраняем изменения
            session.add(task)
            await session.commit()
            return STask.model_validate(task.__dict__)

from sqlalchemy import select

from database import new_session, TaskOrm
from schemas import STaskADD, STask


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
            # Convert TaskOrm objects to dictionaries
            task_dicts = [task_model.__dict__ for task_model in task_models]
            # Validate dictionaries with STask
            task_schemas = [
                STask.model_validate(task_dict) 
                for task_dict in task_dicts
            ]
            return task_schemas

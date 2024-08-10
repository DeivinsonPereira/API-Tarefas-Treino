from typing import Sequence, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from app.core.dependencies import get_session
from app.models.task_model import TaskModel
from app.schemas.task_schema import TaskSchemaBase, TaskSchemaBaseResponse, TaskSchemaUpdate

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TaskSchemaBaseResponse)
async def criar_task(task_criar: TaskSchemaBase, db: AsyncSession = Depends(get_session)):
    task_nova: TaskModel = TaskModel(
        title=task_criar.title,
        subtitle=task_criar.subtitle,
        description=task_criar.description,
        status=task_criar.status,
        task_group_id=task_criar.task_group_id)

    db.add(task_nova)
    await db.commit()
    await db.refresh(task_nova)

    return task_nova


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[TaskSchemaBaseResponse])
async def busca_todas_task(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TaskModel)
        result = await session.execute(query)
        response: Sequence[TaskModel] = result.scalars().unique().all()

        return response


@router.get('/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskSchemaBaseResponse)
async def buscar_por_id(task_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TaskModel).filter(TaskModel.id == task_id)
        result = await session.execute(query)
        response: TaskModel = result.scalar()

        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task não encontrada para esse id')

        return response


@router.put('/{task_id}', status_code=status.HTTP_202_ACCEPTED, response_model=TaskSchemaBaseResponse)
async def atualizar(task_id: int, task_update: TaskSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TaskModel).filter(TaskModel.id == task_id)
        result = await session.execute(query)
        response: TaskModel = result.scalar()

        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task não encontrada para esse id')

        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(response, field, value)

        session.add(response)
        await session.commit()
        await session.refresh(response)

        return response


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove(task_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TaskModel).filter(TaskModel.id == task_id)
        result = await session.execute(query)
        response: TaskModel = result.scalar()

        if not response:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task não encontrada para esse id')

        await session.delete(response)
        await session.commit()



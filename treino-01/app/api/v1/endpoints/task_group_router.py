from typing import List, Sequence

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from app.core.dependencies import get_session
from app.models.task_group_model import TaskGroupModel
from app.schemas.task_group_schema import TaskGroupSchemaBase, TaskGroupSchemaTasks, TaskGroupSchemaResponseTest, \
    TaskGroupSchemaBaseWithId, TaskGroupSchemaUpdate

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TaskGroupSchemaBaseWithId)
async def cria_task_group(task_group_criar: TaskGroupSchemaBase, db: AsyncSession = Depends(get_session)):
    nova_task: TaskGroupModel = TaskGroupModel(
        title=task_group_criar.title,
        description=task_group_criar.description
    )

    db.add(nova_task)
    await db.commit()
    await db.refresh(nova_task)

    return nova_task


@router.get('/', status_code=status.HTTP_200_OK, response_model=TaskGroupSchemaResponseTest)
async def busca_grupos_de_tarefas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TaskGroupModel)
        result = await session.execute(query)
        task_group: Sequence[TaskGroupModel] = result.scalars().unique().all()

        '''
        Transformar o retorno para algo igual ao que é retornado nas apis da vista tecnologia
        
        '''
        task_group_data: List[TaskGroupSchemaTasks] = []

        for item in task_group:
            task_group_data.append(TaskGroupSchemaTasks(**item.__dict__))

        response: TaskGroupSchemaResponseTest = TaskGroupSchemaResponseTest(
            success=True,
            message='Bem sucedido!',
            list=task_group_data
        )

        return response


@router.get('/{id_task_group}', status_code=status.HTTP_200_OK, response_model=TaskGroupSchemaResponseTest)
async def busca_grupos_de_tarefas(id_task_group: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TaskGroupModel).filter(TaskGroupModel.id == id_task_group)
        result = await session.execute(query)
        task_group: TaskGroupModel = result.scalar()

        '''             
        Transformar o retorno para algo igual ao que é retornado nas apis da vista tecnologia
        
        '''

        if not task_group:
            raise HTTPException(detail={'message': 'Task_model não encontrado para este id'},
                                status_code=status.HTTP_404_NOT_FOUND)

        task_group_data = TaskGroupSchemaTasks(**task_group.__dict__)

        response: TaskGroupSchemaResponseTest = TaskGroupSchemaResponseTest(
            success=True,
            message='Bem sucedido!',
            list=[task_group_data]
        )

        return response


@router.put('/{group_id}', status_code=status.HTTP_202_ACCEPTED, response_model=TaskGroupSchemaBaseWithId)
async def atualizar(group_id: int, new_task: TaskGroupSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        if not isinstance(group_id, int):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='O valor do parametro path deve ser um inteiro')

        query = select(TaskGroupModel).filter(TaskGroupModel.id == group_id)
        result = await session.execute(query)
        task_group_searched: TaskGroupModel = result.scalar()

        if not task_group_searched:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task Group não encontrado para este id')

        for field, value in new_task.model_dump(exclude_unset=True).items():
            setattr(task_group_searched, field, value)

        session.add(task_group_searched)
        await session.commit()
        await session.refresh(task_group_searched)

        return task_group_searched


@router.delete('/{group_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_grupo(group_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TaskGroupModel).filter(TaskGroupModel.id == group_id)
        result = await session.execute(query)
        group_task = result.scalar()

        await session.delete(group_task)
        await session.commit()

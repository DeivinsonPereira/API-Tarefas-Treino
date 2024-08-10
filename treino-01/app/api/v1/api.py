from fastapi import APIRouter

from .endpoints import task_router, task_group_router

router = APIRouter()

router.include_router(task_router.router, prefix='/tasks', tags=['Task'])
router.include_router(task_group_router.router, prefix='/tasks_group', tags=['Task Group'])

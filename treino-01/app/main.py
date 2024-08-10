import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI

from api.v1.api import router as router_api
from core.configs import settings

app = FastAPI(title='Treino api', version='0.0.1', description='Api criada para treinar os aprendizados do curso')
app.include_router(router_api, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, log_level='info')

from fastapi import APIRouter

templates_router = APIRouter(prefix='/templates', tags=['templates'])


@templates_router.get('/')
async def add_template():
    return 'ok'

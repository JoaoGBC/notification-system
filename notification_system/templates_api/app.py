from fastapi import FastAPI

from .routers.templatesRouter import templates_router

app = FastAPI()

app.include_router(templates_router)

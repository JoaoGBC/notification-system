from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from .broker import router
from .routers.mail_channel_router import mail_channel_router

app = FastAPI(
    title="public api"
)






app.include_router(mail_channel_router)
app.include_router(router)
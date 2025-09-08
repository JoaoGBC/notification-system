from fastapi import FastAPI, Depends


from .routers.mail_channel_router import mail_channel_router

app = FastAPI()


app.include_router(mail_channel_router)

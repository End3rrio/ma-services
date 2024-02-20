# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from fastapi import FastAPI

from app import rabbitmq
from app.settings import settings

from app.endpoints.recommendation_router import recommendation_router

name = 'Tracks Recommendation Service'

app = FastAPI(title=name)

# @app.on_event('startup')
# def startup():
#     loop = asyncio.get_event_loop()
#     asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(recommendation_router, prefix='/rec-api')

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from fastapi import FastAPI



from app.settings import settings

from app.endpoints.track_router import track_catalog_router


name='TrackCatalog with Recommendations Service'

app = FastAPI(title=name)




# @app.on_event('startup')
# def startup():
#     loop = asyncio.get_event_loop()
#     asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(track_catalog_router, prefix='/track-api')


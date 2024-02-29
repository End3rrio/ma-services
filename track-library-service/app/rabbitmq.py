import json
import random
import traceback
import uuid
from asyncio import AbstractEventLoop
from uuid import UUID
from typing import Dict, Any
from pydantic import BaseModel
import json
import traceback
from aiormq import Connection, Channel
from uuid import UUID
import random

from aio_pika import connect_robust, IncomingMessage, Message
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.models.recomendation import Recomendation
from app.settings import settings

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

async def create_new_recommendation(user_id: UUID, track_id) -> Recomendation:
    return Recomendation(id=uuid.uuid4(), user_id=user_id, recommended_track_id=track_id)


async def send_new_recommendation(connection: Connection, rec: Recomendation):
    channel = await connection.channel()

    message_body = json.dumps(rec.dict(), cls=UUIDEncoder)

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                       "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(rec.dict())


    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='mikhienkov_update_queue'
    )

    await channel.close()


async def send_recommendation(user_id: UUID, track_id: UUID):
    connection = await connect_robust(settings.amqp_url)
    new_recommendation = await create_new_recommendation(user_id, track_id)

    await send_new_recommendation(connection, new_recommendation)
    await connection.close()

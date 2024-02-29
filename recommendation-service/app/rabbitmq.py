import json
import random
import traceback
import uuid
from asyncio import AbstractEventLoop
from uuid import UUID

from aio_pika import connect_robust, IncomingMessage, Message
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.models.recommendation import Recommendation
from app.settings import settings


async def process_new_recommendation(msg: IncomingMessage):
    try:
        print("PROCESSING NEW RECOMMENDATION................")
        data = json.loads(msg.body.decode())
        print(data)
        rec = Recommendation(**data)
        await save_recommendation(rec)
    except Exception as e:
        traceback.print_exc()


async def save_recommendation(rec: Recommendation):
    # Here you would implement your logic to save the recommendation
    # For demonstration, let's just print it
    print(f"Saving recommendation: {rec}")


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    print("Consuming...")

    new_track_queue = await channel.declare_queue('mikhienkov_update_queue', durable=True)

    await new_track_queue.consume(process_new_recommendation)

    print('Started RabbitMQ consuming for the library...')
    return connection

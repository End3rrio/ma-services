# import json
# import random
# import traceback
# import uuid
# from asyncio import AbstractEventLoop
# from uuid import UUID
#
# from aio_pika import connect_robust, IncomingMessage, Message
# from aio_pika.abc import AbstractRobustConnection
# from aio_pika import connect_robust, IncomingMessage
#
# from app.models.recommendation import Recommendation
# from app.models.user import User
# from app.settings import settings
# from app.services.track_catalog_service import TrackCatalogService
# from app.services.recommendation_service import RecommendationService
#
# from app.repositories.track_repo import TrackRepo
# from app.repositories.recommendation_repo import RecommendationRepo
#
#
# async def send_new_recommendation(rec: Recommendation):
#     print(f'Sending recommendation... {rec.json()}')
#     connection = await connect_robust(settings.amqp_url)
#     channel = await connection.channel()
#
#     message_body = json.dumps(rec.json())
#     await channel.default_exchange.publish(
#         Message(body=message_body.encode()),
#         routing_key='uzorov_update_queue'
#     )
#     # Close the channel and connection
#     await channel.close()
#     await connection.close()
#
#
# async def process_new_recommendation(msg: IncomingMessage):
#     try:
#         data = json.loads(msg.body.decode())
#         user_id = data['user_id']
#
#         track_catalog_service = TrackCatalogService(TrackRepo())
#         tracks = track_catalog_service.get_tracks()
#         rec_track = random.choice(tracks)
#
#         recommendation_service = RecommendationService(RecommendationRepo())
#
#         rec = recommendation_service.create_recommendation(user_id=user_id, recommended_track_id=rec_track.id)
#
#         await send_new_recommendation(rec=rec)
#     except:
#         traceback.print_exc()
#
#
# async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
#     connection = await connect_robust(settings.amqp_url, loop=loop)
#     channel = await connection.channel()
#
#     new_track_queue = await channel.declare_queue('uzorov_update_queue', durable=True)
#
#     await new_track_queue.consume(process_new_recommendation)
#
#     print('Started RabbitMQ consuming for the library...')
#     return connection

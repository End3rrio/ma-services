import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body, Response

from app.models.track import Track, CreateTrackRequest
from app.services.music_catalog_service import TrackCatalogService

import prometheus_client

track_catalog_router = APIRouter(prefix='/track-catalog', tags=['TrackCatalog'])

metrics_router = APIRouter(tags=['Metrics'])

get_tracks_count = prometheus_client.Counter(
    "get_tracks_count",
    "Number of get requests for tracks"
)

get_track_count = prometheus_client.Counter(
    "get_track_count",
    "Number of get requests for track by id"
)

add_track_count = prometheus_client.Counter(
    "add_track_count",
    "Number of created tracks"
)
update_track_count = prometheus_client.Counter(
    "update_track_count",
    "Number of updated tracks"
)

delete_track_count = prometheus_client.Counter(
    "delete_track_count",
    "Number of deleted tracks"
)

failed_get_track_count = prometheus_client.Counter(
    "failed_get_track_count",
    "Number of failed attempts to get track by id"
)

name = 'TrackCatalog with Recommendations Service'


@track_catalog_router.get('/')
def get_tracks(track_catalog_service: TrackCatalogService = Depends(TrackCatalogService)) -> list[Track]:
    get_tracks_count.inc(1)
    return track_catalog_service.get_tracks()


# @track_catalog_router.get('/test')
# def get_tracks() -> str:
#     with tracer.start_as_current_span("server_request"):
#         return "it works!"


@track_catalog_router.get('/{track_id}')
def get_track(track_id: UUID, track_catalog_service: TrackCatalogService = Depends(TrackCatalogService)) -> Track:
    track = track_catalog_service.get_track_by_id(track_id)
    if track:
        get_track_count.inc(1)
        return track.dict()
    else:
        failed_get_track_count.inc(1)
        raise HTTPException(404, f'Trackwith id={track_id} not found')


@track_catalog_router.post('/add')
def add_track(request: CreateTrackRequest,
              track_catalog_service: TrackCatalogService = Depends(TrackCatalogService)) -> Track:
    new_track = track_catalog_service.add_track(
        name=request.name,
        author=request.author,
        genre=request.genre,
        description=request.description)
    add_track_count.inc(1)
    return new_track.dict()


@track_catalog_router.put('/update/{track_id}')
def update_track(track_id: UUID, request: CreateTrackRequest,
                 track_catalog_service: TrackCatalogService = Depends(TrackCatalogService)) -> Track:
    updated_track = track_catalog_service.update_track(track_id, request.name, request.author, request.genre,
                                                       request.description)
    update_track_count.inc(1)
    return updated_track.dict()


@track_catalog_router.delete('/delete/{track_id}')
def delete_track(track_id: UUID, track_catalog_service: TrackCatalogService = Depends(TrackCatalogService)) -> None:
    track_catalog_service.delete_track(track_id)
    delete_track_count.inc(1)
    return {'message': 'Track deleted successfully'}

@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )

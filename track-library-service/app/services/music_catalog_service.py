import uuid
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from typing import List
from app.models.track import Track
from app.repositories.bd_tracks_repo import TrackRepo


class TrackCatalogService:
    track_repo: TrackRepo

    def __init__(self, track_repo: TrackRepo = Depends(TrackRepo)) -> None:
        self.track_repo = track_repo

    def get_tracks(self) -> List[Track]:
        return self.track_repo.get_tracks()

    def get_track_by_id(self, track_id: UUID) -> Track:
        return self.track_repo.get_track_by_id(track_id)

    def add_track(self, name: str, author: str, genre: str, description: str) -> Track:
        new_track = Track(id=uuid.uuid4(), name=name, author=author, genre=genre, description=description)
        return self.track_repo.add_track(new_track)

    def update_track(self, track_id: UUID, title: str, author: str, genre: str, publisher: str, description: str) -> Track:
        track = self.track_repo.get_track_by_id(track_id)
        track.name = title
        track.author = author
        track.genre = genre
        track.publisher = publisher
        track.description = description
        return self.track_repo.update_track(track)

    def delete_track(self, track_id: UUID) -> None:
        self.track_repo.delete_track(track_id)

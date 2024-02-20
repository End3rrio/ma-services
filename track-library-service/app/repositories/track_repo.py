from uuid import UUID, uuid4
from typing import List
from app.models.track import Track


class TrackRepo:
    tracks = [
        Track(id=uuid4(), title='TrackTitle', author='Author Name', genre='Fiction',
              publisher='Publisher Name', description='TrackDescription')
    ]

    def __init__(self, clear: bool = False) -> None:

        if clear:
            self.tracks = []

    def get_tracks(self) -> List[Track]:
        return self.tracks

    def get_track_by_id(self, track_id: UUID) -> Track:
        track = next((track for track in self.tracks if track.id == track_id), None)

        if track is not None:
            return track
        else:
            raise KeyError

    def add_track(self, track: Track) -> Track:
        self.tracks.append(track)
        return track

    def update_track(self, track: Track) -> Track:
        existing_track = next((b for b in self.tracks if b.id == track.id), None)
        if existing_track:
            existing_track.name = track.name
            existing_track.author = track.author
            existing_track.genre = track.genre
            existing_track.description = track.description
        return existing_track

    def delete_track(self, track_id: UUID) -> None:
        self.tracks = [track for track in self.tracks if track.id != track_id]

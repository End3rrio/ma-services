import traceback
import uuid
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.track import Track
from app.schemas.track import Track as DTrack


class TrackRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, track: DTrack) -> Track:
        result = Track.from_orm(track)
        # if task.assignee is not 0:
        #     result.assignee = self.assignee_repo.get_assignee_by_id(
        #         task.assignee)

        return result

    def _map_to_schema(self, track: Track) -> DTrack:
        data = dict(track)
        del data['id']
        data['id'] = track.id if track.id is not 0 else 0
        result = DTrack(**data)
        return result

    def get_tracks(self) -> list[Track]:
        tracks = []
        # Track(id=uuid.uuid4(), title="Help me", author="fdafsf", genre="dfsdf", publisher="fdfs", description="dfsd")]

        for b in self.db.query(DTrack).all():
            tracks.append(self._map_to_model(b))
        return tracks

    def get_track_by_id(self, id: UUID) -> Track:
        track = self.db \
            .query(DTrack) \
            .filter(DTrack.id == id) \
            .first()

        if track is None:
            raise KeyError

        return Track.from_orm(track)

    def add_track(self, track: Track) -> Track:
        try:
            db_track = self._map_to_schema(track)
            self.db.add(db_track)
            self.db.commit()
            return self._map_to_model(db_track)
        except:
            traceback.print_exc()
            raise KeyError

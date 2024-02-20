import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.track import Track
from app.repositories.bd_tracks_repo import TrackRepo

sleep(5)


@pytest.fixture()
def track_repo() -> TrackRepo:
    repo = TrackRepo()
    return repo


@pytest.fixture(scope='session')
def first_track() -> Track:
    id = uuid4()
    name = 'Track Name'
    author = 'Author Name'
    genre = 'Genre'
    description = 'Track Description'

    return Track(id=id, name=name, author=author, genre=genre,
                 description=description)


@pytest.fixture(scope='session')
def second_track() -> Track:
    id = uuid4()
    name = 'Second Track Name'
    author = 'Second Author Name'
    genre = 'Comedy'
    description = 'Second Track Description'

    return Track(id=id, name=name, author=author, genre=genre,
                 description=description)


def test_add_first_track(first_track: Track, track_repo: TrackRepo) -> None:
    assert track_repo.add_track(first_track) == first_track


def test_get_track_by_id(first_track: Track, track_repo: TrackRepo) -> None:
    track = track_repo.get_tracks()[0]
    track_by_id = track_repo.get_track_by_id(track.id)
    assert track.id == track_by_id.id


def test_get_track_by_id_error(track_repo: TrackRepo) -> None:
    with pytest.raises(KeyError):
        track_repo.get_track_by_id(uuid4())


def test_add_second_track(first_track: Track, second_track: Track, track_repo: TrackRepo) -> None:
    assert track_repo.add_track(second_track) == second_track
    tracks = track_repo.get_tracks()
    assert tracks[-1] == second_track

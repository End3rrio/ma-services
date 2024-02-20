import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app.services.music_catalog_service import TrackCatalogService
from app.repositories.track_repo import TrackRepo


@pytest.fixture(scope='session')
def track_service() -> TrackCatalogService:
    return TrackCatalogService(TrackRepo(clear=True))


@pytest.fixture()
def track_repo() -> TrackRepo:
    return TrackRepo()


@pytest.fixture(scope='session')
def first_track_data() -> tuple[UUID, str, str, str, str]:
    return uuid4(), 'track1', 'artist1', 'genre1', 'desc1'


@pytest.fixture(scope='session')
def second_track_data() -> tuple[UUID, str, str, str, str]:
    return uuid4(), 'track2', 'artist2', 'genre2', 'desc2'


def test_empty_tracks(track_service: TrackCatalogService) -> None:
    assert track_service.get_tracks() == []


def test_add_track(
        first_track_data,
        track_service: TrackCatalogService
) -> None:
    id, name, author, genre, desc = first_track_data
    track_service.add_track(name, author, genre, desc)
    track = track_service.get_tracks()[0]
    assert track.name == name
    assert track.author == author
    assert track.genre == genre
    assert track.description == desc


def test_add_second_track(
        second_track_data,
        track_service: TrackCatalogService
) -> None:
    id, name, author, genre, desc = second_track_data
    track_service.add_track(name, author, genre, desc)
    track = track_service.get_tracks()[1]
    assert track.name == name
    assert track.author == author
    assert track.genre == genre
    assert track.description == desc


def test_get_tracks_full(
        first_track_data,
        second_track_data,
        track_service: TrackCatalogService
) -> None:
    tracks = track_service.get_tracks()
    assert len(tracks) == 2
    assert tracks[0].name == first_track_data[1]
    assert tracks[1].name == second_track_data[1]


def test_get_tracks(track_service: TrackCatalogService,
                   first_track_data: tuple[UUID, str, str, str, str],
                   second_track_data: tuple[UUID, str, str, str, str]) -> None:
    tracks = track_service.get_tracks()

    # Check that the list of tracks is not empty and contains the expected tracks
    assert tracks
    assert len(tracks) == 2
    # Add tracks via track_service
    _, name1, author1, genre1, desc1 = first_track_data
    _, name2, author2, genre2, desc2 = second_track_data

    track_service.add_track(name1, author1, genre1, desc1)
    track_service.add_track(name2, author2, genre2, desc2)

    tracks_after_addition = track_service.get_tracks()
    assert len(tracks_after_addition) == 4

    # Check that the data of the tracks matches the expected data

    assert tracks_after_addition[2].name == first_track_data[1]
    assert tracks_after_addition[2].author == first_track_data[2]
    assert tracks_after_addition[2].genre == first_track_data[3]
    assert tracks_after_addition[2].description == first_track_data[4]

    assert tracks_after_addition[3].name == second_track_data[1]
    assert tracks_after_addition[3].author == second_track_data[2]
    assert tracks_after_addition[3].genre == second_track_data[3]
    assert tracks_after_addition[3].description == second_track_data[4]


def test_get_track_by_id(track_service: TrackCatalogService,
                        first_track_data: tuple[UUID, str, str, str, str]) -> None:

    track = track_service.get_tracks()[0]
    first_track_id = track.id

    track = track_service.get_track_by_id(first_track_id)

    assert track.name == first_track_data[1]
    assert track.author == first_track_data[2]
    assert track.genre == first_track_data[3]
    assert track.description == first_track_data[4]

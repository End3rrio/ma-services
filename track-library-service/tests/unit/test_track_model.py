import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.track import Track, CreateTrackRequest


def test_track_creation():
    id = uuid4()
    name = 'Track Name'
    author = 'Author Name'
    genre = 'Genre'
    description = 'Track Description'

    track = Track(id=id, name=name, author=author, genre=genre, description=description)

    assert dict(track) == {'id': id, 'name': name, 'author': author,
                           'genre': genre, 'description': description}


def test_track_name_required():
    id = uuid4()
    name = 'Track Name'
    author = 'Author Name'
    genre = 'Genre'
    description = 'Track Description'

    with pytest.raises(ValidationError):
        Track(id=id, author=author, genre=genre, description=description)


def test_track_author_required():
    id = uuid4()
    name = 'Track Name'
    author = 'Author Name'
    genre = 'Genre'
    description = 'Track Description'

    with pytest.raises(ValidationError):
        Track(id=id, name=name, genre=genre, description=description)


def test_track_genre_required():
    id = uuid4()
    name = 'Track Name'
    author = 'Author Name'
    genre = 'Genre'
    description = 'Track Description'

    with pytest.raises(ValidationError):
        Track(id=id, name=name, author=author, description=description)


def test_track_description_required():
    id = uuid4()
    name = 'Track Name'
    author = 'Author Name'
    genre = 'Genre'
    description = 'Track Description'

    with pytest.raises(ValidationError):
        Track(id=id, name=name, author=author, genre=genre)

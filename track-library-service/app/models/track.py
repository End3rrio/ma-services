from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Track(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    author: str
    genre: str
    description: str


class CreateTrackRequest(BaseModel):
    name: str
    author: str
    genre: str
    description: str

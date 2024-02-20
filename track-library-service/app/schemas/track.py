from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base


class Track(Base):
    __tablename__ = 'tracks'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    description = Column(String, nullable=False)

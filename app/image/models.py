# image_frames_server/app/image/models.py
from sqlalchemy import ARRAY, Column, Float, Index, Integer

from ..database import Base


class ImageRow(Base):
    __tablename__ = "image_rows"

    id = Column(Integer, primary_key=True)  # New auto-incrementing primary key
    depth = Column(Float, unique=True)  # Ensuring depth values remain unique
    pixels = Column(ARRAY(Integer, dimensions=1))

    __table_args__ = (
        Index("idx_depth", "depth"),  # Index for optimizing queries based on depth
    )

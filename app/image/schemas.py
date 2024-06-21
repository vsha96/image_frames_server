# image_frames_server/app/image/schemas.py

from pydantic import BaseModel, Field, conlist

from .constants import IMAGE_WIDTH


class ImageRowResponse(BaseModel):
    id: int
    depth: float
    pixels: conlist(int) = Field(default=..., max_length=IMAGE_WIDTH)

# image_frames_server/app/image/router.py
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from matplotlib import pyplot as plt
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .schemas import ImageRowResponse
from .selectors import get_image_rows_by_depth_range
from .utils import fetch_and_prepare_image, is_valid_colormap

router = APIRouter()


@router.get("/image-frame/", response_class=Response)
async def get_image_frame(
    depth_min: float = Query(..., description="Minimum depth"),
    depth_max: float = Query(..., description="Maximum depth"),
    colormap: str = Query(None, description="Optional colormap to apply"),
    db: AsyncSession = Depends(get_db),
):
    if colormap and not is_valid_colormap(colormap):
        raise HTTPException(
            status_code=400,
            detail=f"Colormap '{colormap}' is not supported. Supported colormaps: {', '.join(plt.colormaps())}",
        )

    image_binary = await fetch_and_prepare_image(depth_min, depth_max, db, colormap)

    if not image_binary:
        raise HTTPException(
            status_code=404, detail="No image rows found in the specified depth range"
        )
    return Response(content=image_binary, media_type="image/png")


@router.get("/image-rows-raw/", response_model=list[ImageRowResponse])
async def get_image_rows(
    depth_min: float = Query(..., description="Minimum depth"),
    depth_max: float = Query(..., description="Maximum depth"),
    db: AsyncSession = Depends(get_db),
):
    image_rows = await get_image_rows_by_depth_range(depth_min, depth_max, db)

    if not image_rows:
        raise HTTPException(
            status_code=404, detail="No image rows found in the specified depth range"
        )
    return image_rows

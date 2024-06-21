# image_frames_server/app/image/selectors.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import ImageRow


async def get_image_rows_by_depth_range(
    depth_min: float, depth_max: float, db: AsyncSession
):
    result = await db.execute(
        select(ImageRow)
        .where((ImageRow.depth >= depth_min) & (ImageRow.depth <= depth_max))
        .order_by(ImageRow.depth)
    )
    return result.scalars().all()

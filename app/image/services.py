# image_frames_server/app/image/services.py
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ImageRow


async def store_image_rows(data, db: AsyncSession):
    # Use a transaction for batch insertion
    async with db.begin():
        for item in data:
            image_row = ImageRow(depth=item["depth"], pixels=item["pixels"])
            db.add(image_row)
        # Commit the transaction
        await db.commit()

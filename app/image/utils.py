from io import BytesIO

import matplotlib.pyplot as plt  # Import pyplot which contains the colormaps function
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image
from sqlalchemy.exc import IntegrityError

from ..database import SessionLocal, get_db
from .constants import IMAGE_WIDTH
from .models import ImageRow
from .selectors import get_image_rows_by_depth_range
from .services import store_image_rows


def resize_pixels(pixels, target_length):
    """Resize a list of pixel values to the given target length using linear interpolation."""
    original_length = len(pixels)
    if original_length == target_length:
        return pixels  # No resizing needed if already at the target length
    return (
        np.interp(
            np.linspace(0, original_length - 1, target_length),
            np.arange(original_length),
            pixels,
        )
        .astype(int)
        .tolist()
    )


def read_image_data_from_csv(csv_path: str):
    # Read the CSV file using pandas
    df = pd.read_csv(csv_path)

    # Drop rows where any row element is NaN (blank)
    df = df.dropna()

    # Check if all rows have the same number of elements
    row_length = df.apply(lambda x: len(x), axis=1)
    if not row_length.nunique() == 1:
        raise ValueError("All rows must have the same number of columns")

    # Convert DataFrame rows to a list of dictionaries
    data = []
    for index, row in df.iterrows():
        try:
            # Assuming 'depth' is the first column and it is a valid float
            depth = float(row["depth"])
            # Ensures all elements are valid integers (or convertible to int)
            original_pixels = [int(pixel) for pixel in row[1:].tolist()]
            # Resize the pixel data
            resized_pixels = resize_pixels(original_pixels, IMAGE_WIDTH)

            data.append({"depth": depth, "pixels": resized_pixels})
        except ValueError as e:
            raise IntegrityError(f"Error processing row {index}: {e}")

    return data


async def import_csv_to_db(csv_file: str):
    # Read data from CSV
    data = read_image_data_from_csv(csv_file)
    # Create a new session
    async with SessionLocal() as session:
        await store_image_rows(data, session)


def is_valid_colormap(colormap):
    """Check if the provided colormap name is in the list of supported matplotlib colormaps."""
    return colormap and colormap in plt.colormaps()


def apply_colormap_to_image(image_array, colormap):
    if colormap:
        # Normalize the image array to be between 0 and 1
        norm = Normalize(vmin=image_array.min(), vmax=image_array.max())
        # Apply the colormap
        mapping = plt.get_cmap(colormap)
        colored_image = mapping(norm(image_array))
        # Convert to 8-bit per channel format
        image_array = (colored_image[:, :, :3] * 255).astype(np.uint8)
    return image_array


def create_image_from_rows(image_data, colormap=None):
    """Convert a list of pixel rows into a binary PNG image, optionally applying a color map."""
    height = len(image_data)
    width = len(image_data[0]) if height > 0 else 0
    image_array = np.array(image_data, dtype=np.uint8)

    # Apply color map if specified
    image_array = apply_colormap_to_image(image_array, colormap)

    # Create an image from the numpy array
    img = Image.fromarray(image_array)
    byte_io = BytesIO()
    img.save(byte_io, "PNG")
    byte_io.seek(0)
    return byte_io.getvalue()


async def fetch_and_prepare_image(
    depth_min: float, depth_max: float, db, colormap=None
):
    """Fetch image rows by depth range and prepare an image."""
    image_rows = await get_image_rows_by_depth_range(depth_min, depth_max, db)
    if not image_rows:
        return None

    # Create an image from image row data
    image_data = [row.pixels for row in image_rows]
    return create_image_from_rows(image_data, colormap)

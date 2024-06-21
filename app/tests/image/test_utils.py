import pytest

from app.image.utils import resize_pixels

# Define a list of test cases
test_cases = [
    ([10, 20, 30], 5, [10, 15, 20, 25, 30]),  # Increase size
    ([10, 20, 30, 40, 50, 60], 3, [10, 35, 60]),  # Decrease size
    ([15, 25, 35], 3, [15, 25, 35]),  # Same size
]


@pytest.mark.parametrize("original_pixels, target_length, expected", test_cases)
def test_resize_pixels(original_pixels, target_length, expected):
    resized = resize_pixels(original_pixels, target_length)
    assert len(resized) == len(expected), "Resized list should match the target length"
    assert resized == expected, "Resized list values should match the expected values"

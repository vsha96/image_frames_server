from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.image.models import ImageRow
from app.image.selectors import get_image_rows_by_depth_range


@pytest.fixture
async def mock_db_session():
    session = AsyncMock(spec=AsyncSession)
    mock_result = AsyncMock()
    session.execute.return_value = mock_result
    return session, mock_result


class TestSelectors:
    @pytest.mark.asyncio
    async def test_get_image_rows_by_depth_range(self, mock_db_session):
        session, mock_result = await mock_db_session
        expected_rows = [ImageRow(depth=10.0, pixels=[1, 2, 3])]  # Example data
        mock_result.scalars.return_value.all.return_value = expected_rows

        result = await get_image_rows_by_depth_range(5.0, 15.0, session)

        session.execute.assert_called_once()
        assert result == expected_rows, "The returned rows do not match expected rows"

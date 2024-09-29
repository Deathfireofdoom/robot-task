import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db_session


@pytest.mark.asyncio
async def test_get_db_session_success():
    mock_session = AsyncMock(spec=AsyncSession)

    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = AsyncMock()

    with patch(
        "src.core.database.async_session",
        return_value=AsyncMock(
            __aenter__=mock_session.__aenter__, __aexit__=mock_session.__aexit__
        ),
    ):
        async for session in get_db_session():
            assert session == mock_session

        mock_session.commit.assert_called_once()

        mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_get_db_session_rollback_on_commit_error():
    mock_session = AsyncMock(spec=AsyncSession)

    mock_session.commit.side_effect = Exception("Commit failed")

    mock_session.__aenter__.return_value = mock_session
    mock_session.__aexit__.return_value = AsyncMock()

    with patch("src.core.database.async_session", return_value=mock_session):
        async for session in get_db_session():
            session.add(AsyncMock())

        with pytest.raises(Exception, match="Commit failed"):
            await mock_session.commit()

        mock_session.rollback.assert_called_once()

        mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_get_db_session_connection_error():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.__aenter__.side_effect = Exception("Could not connect to the database")

    with patch(
        "src.core.database.async_session",
        return_value=AsyncMock(
            __aenter__=mock_session.__aenter__, __aexit__=mock_session.__aexit__
        ),
    ):
        with pytest.raises(Exception, match="Could not connect to the database"):
            async for session in get_db_session():
                pass

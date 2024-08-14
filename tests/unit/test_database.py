from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncEngine

from src.database import create_tables, delete_tables
from src.database import Base


async def test_create_tables(mocker):
    mock_conn = AsyncMock()
    mock_begin = mocker.patch.object(
        AsyncEngine,
        'begin',
        return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_conn))
    )
    mock_run_sync = mocker.patch.object(mock_conn, 'run_sync', new_callable=AsyncMock)

    await create_tables()

    mock_begin.assert_called_once()
    mock_run_sync.assert_called_once_with(Base.metadata.create_all)


async def test_delete_tables(mocker):
    mock_conn = AsyncMock()
    mock_begin = mocker.patch.object(AsyncEngine, 'begin', return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_conn)))
    mock_run_sync = mocker.patch.object(mock_conn, 'run_sync', new_callable=AsyncMock)

    await delete_tables()

    mock_begin.assert_called_once()
    mock_run_sync.assert_called_once_with(Base.metadata.drop_all)

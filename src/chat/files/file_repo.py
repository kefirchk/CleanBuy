from sqlalchemy import select

from src.chat.models import FileOrm
from src.database import new_session


class FileRepo:
    @staticmethod
    async def get_file_by_url(file_url: str) -> FileOrm:
        async with new_session() as session:
            query = select(FileOrm).where(FileOrm.file_url == file_url)

            result = await session.execute(query)
            file_orm = result.scalar_one_or_none()

            return file_orm

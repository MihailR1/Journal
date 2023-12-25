import sqlalchemy

from app.database import async_session_factory
from app.models import Estimation


class BasicCRUD:
    @staticmethod
    async def find_all(model):
        query = sqlalchemy.select(model)

        async with async_session_factory() as session:
            result = await session.execute(query)

        return result.unique().scalars().all()

    @staticmethod
    async def add_score(student_id: int, lesson_id: int, score: int, model=Estimation):
        query = (
            sqlalchemy.insert(model)
            .values(number=score, lesson_id=lesson_id, student_id=student_id)
            .returning(model.__table__.columns)
        )

        async with async_session_factory() as session:
            result = await session.execute(query)
            await session.commit()

        return result.unique().scalars().all()

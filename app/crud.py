import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_factory
from app.models import Estimation


class BasicCRUD:
    @staticmethod
    async def _execute(query, commit: bool = False):
        async with async_session_factory() as session:
            try:
                result = await session.execute(query)

                if commit is True:
                    await session.commit()

            except SQLAlchemyError:
                await session.rollback()
                raise SQLAlchemyError

        return result

    @staticmethod
    async def get_all(model):
        query = sqlalchemy.select(model)

        result = await BasicCRUD._execute(query)

        return result.unique().scalars().all()

    @staticmethod
    async def add_score(student_id: int, lesson_id: int, score: int, model=Estimation):
        query = (
            sqlalchemy.insert(model)
            .values(number=score, lesson_id=lesson_id, student_id=student_id)
            .returning(model.__table__.columns)
        )

        result = await BasicCRUD._execute(query, commit=True)

        return result.unique().scalars().all()

    @staticmethod
    async def add_data_bulk(
        data_for_insert: list[dict[str, str]] | list[dict[str, object]], model=Estimation
    ):
        async with async_session_factory() as session:
            await session.execute(sqlalchemy.insert(model), data_for_insert)
            await session.commit()

        return None

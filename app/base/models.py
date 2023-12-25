from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} - id={self.id}'

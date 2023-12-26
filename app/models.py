from datetime import datetime
from typing import List

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} - id={self.id}"


class SchoolClass(Base):
    __tablename__ = "class"
    name: Mapped[str]
    students: Mapped[List["Student"]] = relationship(back_populates="school_class", lazy="joined")


class Student(Base):
    __tablename__ = "students"
    name: Mapped[str]
    second_name: Mapped[str]
    class_id: Mapped[int] = mapped_column(ForeignKey("class.id"))
    school_class: Mapped["SchoolClass"] = relationship(back_populates="students", lazy="joined")
    scores: Mapped[List["Estimation"]] = relationship(back_populates="student", lazy="joined")


class Lesson(Base):
    __tablename__ = "lessons"
    name: Mapped[str]
    scores: Mapped[List["Estimation"]] = relationship(back_populates="lesson", lazy="joined")


class Estimation(Base):
    __tablename__ = "estimation"
    number: Mapped[int]
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    lesson: Mapped["Lesson"] = relationship(back_populates="scores", lazy="joined")
    student: Mapped["Student"] = relationship(back_populates="scores", lazy="joined")

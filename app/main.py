import random

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.crud import BasicCRUD
from app.models import Lesson, SchoolClass, Student
from app.utils import generate_classes, generate_lessons, generate_students

app = FastAPI()

templates = Jinja2Templates(directory=f"{settings.BASEDIR}/templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    all_students = await BasicCRUD.get_all(Student)
    all_lessons = await BasicCRUD.get_all(Lesson)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "students": all_students, "lessons": all_lessons},
    )


@app.post("/update_score/")
async def update_score(
    request: Request,
    user_id: int = Form(),
    lesson_id: int = Form(),
    score: int = Form(ge=1, le=5),
):
    await BasicCRUD.add_score(user_id, lesson_id, score)

    return await main(request)


@app.get("/generate_data")
async def generate_data(number_students: int = 150, number_of_classes: int = 10) -> None:
    lessons = [{"name": lesson} for lesson in await generate_lessons()]
    classes = [{"name": school_class} for school_class in await generate_classes(number_of_classes)]
    students = [
        {
            "name": stud[0],
            "second_name": stud[1],
            "class_id": random.randint(1, number_of_classes),
        }
        for stud in await generate_students(number_students)
    ]

    await BasicCRUD.add_data_bulk(lessons, Lesson)
    await BasicCRUD.add_data_bulk(classes, SchoolClass)
    await BasicCRUD.add_data_bulk(students, Student)

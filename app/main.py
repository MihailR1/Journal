from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.crud import BasicCRUD
from app.config import settings
from app.models import Student, Lesson

app = FastAPI()

templates = Jinja2Templates(directory=f"{settings.BASEDIR}/templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    all_students = await BasicCRUD.find_all(Student)
    all_lessons = await BasicCRUD.find_all(Lesson)

    return templates.TemplateResponse(
        "index.html", {"request": request, "students": all_students, "lessons": all_lessons}
    )


@app.post("/update_score/")
async def update_score(
    user_id: int = Form(), lesson_id: int = Form(), score: int = Form(ge=1, le=5)
):
    update = await BasicCRUD.add_score(user_id, lesson_id, score)
    return update

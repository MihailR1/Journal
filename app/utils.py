import random

import faker


async def generate_classes(number: int = 20) -> list[str]:
    letter = ["А", "Б", "В", "Г", "Д"]
    result = [f"{random.randint(1, 11)}{random.choice(letter)}" for _ in range(number)]

    return result


async def generate_students(number: int = 20) -> list[tuple[str, str]]:
    fake = faker.Faker(["ru-RU"])
    result = [(fake.first_name(), fake.last_name()) for _ in range(number)]

    return result


async def generate_lessons() -> list[str]:
    lessons = [
        "Математика",
        "Алгебра",
        "Геометрия",
        "Информа́тика",
        "Окружающий мир",
        "География",
        "Биология",
        "Физика",
        "Химия",
        "Русский",
        "Английский",
    ]

    return lessons

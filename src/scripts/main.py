import asyncio
import json
import sys
from pathlib import Path

from pydantic import BaseModel

from models import Teacher
from schemes.request import StudentCreateRequest
from schemes.request.teacher import TeacherCreateRequest
from src.models import Student
from src.session import async_session_maker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def load_students_from_json(json_path: str):
    """
    Загрузка учеников из JSON файла в базу данных
    """
    try:
        # Читаем JSON файл
        with open(json_path, 'r', encoding='utf-8') as f:
            students_data = json.load(f)

        logger.info(f"Загружено {len(students_data)} записей из JSON")

        # Создаем сессию и добавляем записи
        async with async_session_maker() as session:
            async with session.begin():
                for student_data in students_data:
                    student = StudentCreateRequest.model_validate(student_data)
                    session.add( Student(**student.model_dump()))

                # Здесь не нужно явно коммитить, session.begin() сделает autoflush

            logger.info("✅ Данные успешно загружены в базу данных")

    except FileNotFoundError:
        logger.error(f"❌ Файл {json_path} не найден")
    except json.JSONDecodeError as e:
        logger.error(f"❌ Ошибка парсинга JSON: {e}")
    except Exception as e:
        logger.error(f"❌ Непредвиденная ошибка: {e}")

async def load_teachers_from_json(json_path: str):
    """
    Загрузка учителей из JSON файла в базу данных
    """
    try:
        # Читаем JSON файл
        with open(json_path, 'r', encoding='utf-8') as f:
            teachers_data = json.load(f)

        logger.info(f"Загружено {len(teachers_data)} записей из JSON")

        # Создаем сессию и добавляем записи
        async with async_session_maker() as session:
            async with session.begin():
                for teacher_data in teachers_data:
                    teacher = TeacherCreateRequest.model_validate(teacher_data)
                    session.add( Teacher(**teacher.model_dump()))

                # Здесь не нужно явно коммитить, session.begin() сделает autoflush

            logger.info("✅ Данные успешно загружены в базу данных")

    except FileNotFoundError:
        logger.error(f"❌ Файл {json_path} не найден")
    except json.JSONDecodeError as e:
        logger.error(f"❌ Ошибка парсинга JSON: {e}")
    except Exception as e:
        logger.error(f"❌ Непредвиденная ошибка: {e}")


async def main():
    """
    Основная функция для запуска загрузки
    """

    student_json_file = Path() / "src/scripts/student.json"
    logger.info(f"Начинаем загрузку из файла: {student_json_file}")
    await load_students_from_json(student_json_file)

    teacher_json_file = Path() / "src/scripts/teacher.json"
    logger.info(f"Начинаем загрузку из файла: {teacher_json_file}")
    await load_teachers_from_json(teacher_json_file)

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
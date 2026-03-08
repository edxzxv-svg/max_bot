import asyncio
import json
import logging
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError

from src.models import Schedule, Student, Teacher
from src.schemes.request import ScheduleCreateRequest, StudentCreateRequest
from src.schemes.request.teacher import TeacherCreateRequest
from src.session import async_session_maker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def load_students_from_json(json_path: Path) -> None:
    """Загрузка учеников из JSON файла в базу данных."""
    try:
        with Path.open(json_path, encoding="utf-8") as f:
            students_data = json.load(f)

        logger.info("Загружено %s записей из JSON", len(students_data))

        async with async_session_maker() as session:
            async with session.begin():
                for student_data in students_data:
                    student = StudentCreateRequest.model_validate(student_data)
                    session.add( Student(**student.model_dump()))

            logger.info("✅ Данные успешно загружены в базу данных")

    except FileNotFoundError:
        logger.exception("❌ Файл %s не найден", json_path)
    except json.JSONDecodeError:
        logger.exception("❌ Ошибка парсинга JSON")
    except Exception:
        logger.exception("❌ Непредвиденная ошибка")

async def load_teachers_from_json(json_path: Path) -> None:
    """Загрузка учителей из JSON файла в базу данных."""
    try:
        with Path.open(json_path, encoding="utf-8") as f:
            teachers_data = json.load(f)

        logger.info("Загружено %s записей из JSON", len(teachers_data))

        async with async_session_maker() as session:
            async with session.begin():
                for teacher_data in teachers_data:
                    teacher = TeacherCreateRequest.model_validate(teacher_data)
                    session.add( Teacher(**teacher.model_dump()))

            logger.info("✅ Данные успешно загружены в базу данных")

    except FileNotFoundError:
        logger.exception("❌ Файл %s не найден", json_path)
    except json.JSONDecodeError:
        logger.exception("❌ Ошибка парсинга JSON")
    except Exception:
        logger.exception("❌ Непредвиденная ошибка")


async def load_schedule_from_json(json_path: Path) -> None: # noqa: PLR0915, PLR0912
    """Загрузка расписания из JSON файла в базу данных."""
    try:
        with Path.open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        schedule_records = []

        day_map = {
            "ПОНЕДЕЛЬНИК": 1,
            "ВТОРНИК": 2,
            "СРЕДА": 3,
            "ЧЕТВЕРГ": 4,
            "ПЯТНИЦА": 5,
            "СУББОТА": 6
        }

        for day_data in data.get("schedule", []):
            day_name = day_data.get("day")
            day_number = day_map.get(day_name, 0)

            if day_number == 0:
                logger.warning("Неизвестный день недели: %s", day_name)
                continue

            for lesson in day_data.get("lessons", []):
                lesson_number = lesson.get("lesson_number")

                for class_data in lesson.get("classes", []):
                    class_str = class_data.get("class")
                    if not class_str or len(class_str) < 2: # noqa: PLR2004
                        continue

                    try:
                        class_number = int(class_str[:-1])
                        class_parallel = class_str[-1]
                    except (ValueError, IndexError):
                        logger.warning(
                            "Некорректный формат класса: %s",
                            class_str,
                        )
                        continue

                    subject = class_data.get("subject")
                    if not subject or subject.strip() == "":
                        continue

                    room = class_data.get("room")
                    # Преобразуем room в int или None
                    if room is None or room == "":
                        room_value = None
                    else:
                        try:
                            if isinstance(room, str) and "/" in room:
                                room_value = int(room.split("/")[0])
                            else:
                                room_value = int(room)
                        except (ValueError, TypeError):
                            logger.warning(
                                "Некорректный номер кабинета: "
                                "%s для класса %s",
                                room,
                                class_str,
                            )
                            room_value = None

                    schedule_records.append({
                        "uuid": uuid4(),
                        "class_number": class_number,
                        "class_parallel": class_parallel,
                        "day_of_week": day_number,
                        "lesson_number": lesson_number,
                        "subject": subject.strip(),
                        "room": room_value
                    })

        logger.info("Загружено %s записей из JSON", len(schedule_records))

        async with async_session_maker() as session, session.begin():
            for row in schedule_records:
                try:
                    schedule_valid = ScheduleCreateRequest.model_validate(row)
                    schedule_db = Schedule(**schedule_valid.model_dump())

                    session.add(schedule_db)
                except ValidationError:
                    logger.exception("Ошибка валидации записи %s", row)
                    continue

        logger.info("✅ Данные успешно загружены в базу данных")

    except FileNotFoundError:
        logger.exception("❌ Файл %s не найден", json_path)
    except json.JSONDecodeError:
        logger.exception("❌ Ошибка парсинга JSON")
    except Exception:
        logger.exception("❌ Непредвиденная ошибка")
        raise


async def main() -> None:
    """Основная функция для запуска загрузки."""
    student_json_file = Path() / "src/scripts/student.json"
    logger.info("Начинаем загрузку из файла: %s", student_json_file)
    await load_students_from_json(student_json_file)

    teacher_json_file = Path() / "src/scripts/teacher.json"
    logger.info("Начинаем загрузку из файла: %s", teacher_json_file)
    await load_teachers_from_json(teacher_json_file)

    schedule_json_file = Path() / "src/scripts/schedule_8.json"
    logger.info("Начинаем загрузку из файла: %s", schedule_json_file)
    await load_schedule_from_json(schedule_json_file)

if __name__ == "__main__":
    asyncio.run(main())

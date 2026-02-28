import asyncio
import json
from pathlib import Path
from uuid import uuid4

from pydantic import ValidationError

from src.schemes.request import StudentCreateRequest, ScheduleCreateRequest
from src.schemes.request.teacher import TeacherCreateRequest
from src.models import Student, Teacher, Schedule
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


async def load_schedule_from_json(json_path: str):
    """
    Загрузка расписания из JSON файла в базу данных
    """
    try:
        # Читаем JSON файл
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Преобразуем структуру JSON в плоский список записей
        schedule_records = []

        # Маппинг дней недели
        day_map = {
            'ПОНЕДЕЛЬНИК': 1,
            'ВТОРНИК': 2,
            'СРЕДА': 3,
            'ЧЕТВЕРГ': 4,
            'ПЯТНИЦА': 5,
            'СУББОТА': 6
        }

        for day_data in data.get('schedule', []):
            day_name = day_data.get('day')
            day_number = day_map.get(day_name, 0)

            if day_number == 0:
                logger.warning(f"Неизвестный день недели: {day_name}")
                continue

            for lesson in day_data.get('lessons', []):
                lesson_number = lesson.get('lesson_number')

                for class_data in lesson.get('classes', []):
                    class_str = class_data.get('class')
                    if not class_str or len(class_str) < 2:
                        continue

                    # Парсим класс (например "5А" -> 5 и "А")
                    try:
                        class_number = int(class_str[:-1])
                        class_parallel = class_str[-1]
                    except (ValueError, IndexError):
                        logger.warning(f"Некорректный формат класса: {class_str}")
                        continue

                    subject = class_data.get('subject')
                    if not subject or subject.strip() == "":
                        continue

                    room = class_data.get('room')
                    # Преобразуем room в int или None
                    if room is None or room == "":
                        room_value = None
                    else:
                        try:
                            # Некоторые комнаты могут быть строками типа "24/32"
                            # В этом случае берем первое число или сохраняем как строку
                            # Но ваша модель ожидает int, поэтому нужно решение
                            if isinstance(room, str) and '/' in room:
                                room_value = int(room.split('/')[0])
                            else:
                                room_value = int(room)
                        except (ValueError, TypeError):
                            logger.warning(f"Некорректный номер кабинета: {room} для класса {class_str}")
                            room_value = None

                    schedule_records.append({
                        'uuid': uuid4(),
                        'class_number': class_number,
                        'class_parallel': class_parallel,
                        'day_of_week': day_number,
                        'lesson_number': lesson_number,
                        'subject': subject.strip(),
                        'room': room_value
                    })

        logger.info(f"Загружено {len(schedule_records)} записей из JSON")

        async with async_session_maker() as session:
            async with session.begin():
                for row in schedule_records:
                    try:
                        schedule_validated = ScheduleCreateRequest.model_validate(row)
                        schedule_db = Schedule(**schedule_validated.model_dump())

                        session.add(schedule_db)
                    except ValidationError as e:
                        logger.error(f"Ошибка валидации записи {row}: {e}")
                        continue

            # session.begin() автоматически сделает commit при успешном завершении

        logger.info("✅ Данные успешно загружены в базу данных")

    except FileNotFoundError:
        logger.error(f"❌ Файл {json_path} не найден")
    except json.JSONDecodeError as e:
        logger.error(f"❌ Ошибка парсинга JSON: {e}")
    except Exception as e:
        logger.error(f"❌ Непредвиденная ошибка: {e}")
        raise


async def main():
    """
    Основная функция для запуска загрузки
    """

    # student_json_file = Path() / "src/scripts/student.json"
    # logger.info(f"Начинаем загрузку из файла: {student_json_file}")
    # await load_students_from_json(student_json_file)
    #
    # teacher_json_file = Path() / "src/scripts/teacher.json"
    # logger.info(f"Начинаем загрузку из файла: {teacher_json_file}")
    # await load_teachers_from_json(teacher_json_file)

    schedule_json_file = Path() / "src/scripts/schedule_8.json"
    logger.info(f"Начинаем загрузку из файла: {schedule_json_file}")
    await load_schedule_from_json(schedule_json_file)

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
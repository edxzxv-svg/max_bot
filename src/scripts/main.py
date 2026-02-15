import asyncio
import json
import sys
from pathlib import Path
from schemes.request import StudentCreateRequest
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


async def main():
    """
    Основная функция для запуска загрузки
    """
    # Путь к JSON файлу (можно изменить или передавать как аргумент)
    json_file = Path() / "src/scripts/student.json"
    print(json_file.absolute())

    # Проверяем, есть ли аргумент командной строки
    if len(sys.argv) > 1:
        json_file = sys.argv[1]

    logger.info(f"Начинаем загрузку из файла: {json_file}")
    await load_students_from_json(json_file)


if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
from gigachat import Function, FunctionParameters
from gigachat.models.chat import FunctionParametersProperty

SCHEDULE_FUNCTION = Function(
    name="get_schedule",
    description="Возвращает расписание уроков по заданным "
                "параметрам поиска (класс, параллель, день недели, "
                "номер урока, предмет, кабинет)",
    parameters=FunctionParameters(
        type="object",
        properties={
            "class_numbers": FunctionParametersProperty(
                type="array",
                items={"type": "integer"},
                description="Номера классов для фильтрации (от 0 до 11)"
            ),
            "class_parallels": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Буквы параллелей классов (А, Б, В и т.д.)"
            ),
            "day_of_weeks": FunctionParametersProperty(
                type="array",
                items={"type": "integer"},
                description="Дни недели для фильтрации "
                           "(1 - понедельник, 7 - воскресенье)"
            ),
            "lesson_numbers": FunctionParametersProperty(
                type="array",
                items={"type": "integer"},
                description="Номера уроков для фильтрации (от 1 до 24)"
            ),
            "subjects": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Названия предметов для фильтрации"
            ),
            "rooms": FunctionParametersProperty(
                type="array",
                items={"type": "integer"},
                description="Номера кабинетов для фильтрации"
            )
        }
    ),
    return_parameters={
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["success", "failed"],
                "description": "Статус выполнения запроса"
            },
            "detail": {
                "type": "string",
                "description": "Детальное описание результата "
                              "(например, 'Найдено 5 записей')"
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "class_number": {
                            "type": "integer",
                            "description": "Номер класса"
                        },
                        "class_parallel": {
                            "type": "string",
                            "description": "Буква параллели"
                        },
                        "lesson_number": {
                            "type": "integer",
                            "description": "Номер урока по порядку"
                        },
                        "day_of_week": {
                            "type": "integer",
                            "description": "День недели (1-7)"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Название предмета"
                        },
                        "room": {
                            "type": "integer",
                            "nullable": True,
                            "description": "Номер кабинета"
                        }
                    }
                },
                "description": "Список записей расписания, "
                              "соответствующих критериям поиска"
            }
        }
    }
)

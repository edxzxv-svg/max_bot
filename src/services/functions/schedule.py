SCHEDULE_FUNCTION = {
    "name": "get_schedule",
    "description": "Возвращает расписание уроков по заданным параметрам поиска (класс, параллель, день недели, номер урока, предмет, кабинет)",
    "parameters": {
        "type": "object",
        "properties": {
            "class_numbers": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Номера классов для фильтрации (от 0 до 11)",
                "examples": [9, 8, 5]
            },
            "class_parallels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Буквы параллелей классов (А, Б, В и т.д.)",
                "examples": ["А", "Б", "В"]
            },
            "day_of_weeks": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Дни недели для фильтрации (1 - понедельник, 7 - воскресенье)",
                "examples": [1, 2, 3]
            },
            "lesson_numbers": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Номера уроков для фильтрации (от 1 до 24)",
                "examples": [1, 2, 3]
            },
            "subjects": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Названия предметов для фильтрации",
                "examples": ["Математика", "Физика", "Русский язык"]
            },
            "rooms": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Номера кабинетов для фильтрации",
                "examples": [24, 8, 101]
            }
        }
    },
    "return_parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["success", "failed"],
                "description": "Статус выполнения запроса"
            },
            "detail": {
                "type": "string",
                "description": "Детальное описание результата (например, 'Найдено 5 записей')"
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
                "description": "Список записей расписания, соответствующих критериям поиска"
            }
        }
    }
}
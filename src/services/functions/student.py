STUDENT_LIST_FUNCTION = {
    "name": "get_student_list",
    "description": "Возвращает данные учеников (ФИО, класс, день рождение) по заданным параметрам поиска",
    "parameters": {
        "type": "object",
        "properties": {
            "first_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Фамилии учеников для поиска"
            },
            "last_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Имена учеников для поиска"
            },
            "second_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Отчества учеников для поиска"
            },
            "start_date": {
                "type": "string",
                "format": "date",
                "description": "Начало периода поиска (ГГГГ-ММ-ДД)"
            },
            "end_date": {
                "type": "string",
                "format": "date",
                "description": "Конец периода поиска (ГГГГ-ММ-ДД)"
            },
            "class_numbers": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Номера классов для фильтрации"
            },
            "class_parallels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Буквы параллелей классов"
            }
        }
    },
    "return_parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["success", "failed"],
                "description": "Статус выполнения"
            },
            "detail": {
                "type": "string",
                "description": "Описание результата"
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "full_name": {"type": "string"},
                        "birth_day": {"type": "string"},
                        "class_number": {"type": "integer"},
                        "class_parallel": {"type": "string"}
                    }
                },
                "description": "Список учеников"
            }
        }
    }
}
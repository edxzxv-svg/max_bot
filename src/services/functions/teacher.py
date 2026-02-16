TEACHER_LIST_FUNCTION = {
    "name": "get_teacher_list",
    "description": "Возвращает данные учителей "
                   "(ФИО, день рождение, уровень образования) "
                   "по заданным параметрам поиска",
    "parameters": {
        "type": "object",
        "properties": {
            "first_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Фамилии учителей для поиска"
            },
            "last_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Имена учителей для поиска"
            },
            "second_names": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Отчества учителей для поиска"
            },
            "birth_day_ge": {
                "type": "string",
                "format": "date",
                "description": "Начало периода поиска дня рождения (ГГГГ-ММ-ДД)"
            },
            "birth_day_le": {
                "type": "string",
                "format": "date",
                "description": "Конец периода поиска  дня рождения (ГГГГ-ММ-ДД)"
            },
            "employment_date_ge": {
                "type": "string",
                "format": "date",
                "description": "Начало периода поиска по дате трудоустройства (ГГГГ-ММ-ДД)"
            },
            "employment_date_le": {
                "type": "string",
                "format": "date",
                "description": "Конец периода поиска по дате трудоустройства (ГГГГ-ММ-ДД)"
            },
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
                        "employment_date": {"type": "string"},
                        "education": {"type": "string"}
                    }
                },
                "description": "Список учителей"
            }
        }
    }
}
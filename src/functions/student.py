from gigachat import Function, FunctionParameters
from gigachat.models.chat import FunctionParametersProperty

STUDENT_LIST_FUNCTION = Function(
    name="get_student_list",
    description="Возвращает данные учеников (ФИО, класс, день рождение) "
                "по заданным параметрам поиска",
    parameters=FunctionParameters(
        type="object",
        properties={
            "first_names": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Фамилии учеников для поиска"
            ),
            "last_names": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Имена учеников для поиска"
            ),
            "second_names": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Отчества учеников для поиска"
            ),
            "start_date": FunctionParametersProperty(
                type="string",
                description="Начало периода поиска (ГГГГ-ММ-ДД)"
            ),
            "end_date": FunctionParametersProperty(
                type="string",
                description="Конец периода поиска (ГГГГ-ММ-ДД)"
            ),
            "class_numbers": FunctionParametersProperty(
                type="array",
                items={"type": "integer"},
                description="Номера классов для фильтрации"
            ),
            "class_parallels": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Буквы параллелей классов"
            )
        }
    ),
    return_parameters={
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
                        "full_name": {
                            "type": "string",
                            "description": "Полное имя ученика"
                        },
                        "birth_day": {
                            "type": "string",
                            "format": "date",
                            "description": "Дата рождения"
                        },
                        "class_number": {
                            "type": "integer",
                            "description": "Номер класса"
                        },
                        "class_parallel": {
                            "type": "string",
                            "description": "Буква параллели"
                        }
                    }
                },
                "description": "Список учеников"
            }
        }
    }
)

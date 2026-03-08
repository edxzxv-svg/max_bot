from gigachat import Function, FunctionParameters
from gigachat.models.chat import FunctionParametersProperty

TEACHER_LIST_FUNCTION = Function(
    name="get_teacher_list",
    description="Возвращает данные учителей "
                "(ФИО, день рождение, уровень образования) "
                "по заданным параметрам поиска",
    parameters=FunctionParameters(
        type="object",
        properties={
            "first_names": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Фамилии учителей для поиска"
            ),
            "last_names": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Имена учителей для поиска"
            ),
            "second_names": FunctionParametersProperty(
                type="array",
                items={"type": "string"},
                description="Отчества учителей для поиска"
            ),
            "birth_day_ge": FunctionParametersProperty(
                type="string",
                description="Начало периода поиска "
                           "дня рождения (ГГГГ-ММ-ДД)"
            ),
            "birth_day_le": FunctionParametersProperty(
                type="string",
                description="Конец периода поиска "
                           "дня рождения (ГГГГ-ММ-ДД)"
            ),
            "employment_date_ge": FunctionParametersProperty(
                type="string",
                description="Начало периода поиска по дате "
                           "трудоустройства (ГГГГ-ММ-ДД)"
            ),
            "employment_date_le": FunctionParametersProperty(
                type="string",
                description="Конец периода поиска по дате "
                           "трудоустройства (ГГГГ-ММ-ДД)"
            ),
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
                            "description": "Полное имя учителя"
                        },
                        "birth_day": {
                            "type": "string",
                            "format": "date",
                            "description": "Дата рождения"
                        },
                        "employment_date": {
                            "type": "string",
                            "format": "date",
                            "description": "Дата трудоустройства"
                        },
                        "education": {
                            "type": "string",
                            "description": "Уровень образования"
                        }
                    }
                },
                "description": "Список учителей"
            }
        }
    }
)

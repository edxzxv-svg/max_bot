from gigachat import Function, FunctionParameters
from gigachat.models.chat import FunctionParametersProperty

CALL_LIST_FUNCTION = Function(
    name="get_calls",
    description="Возвращает расписание звонков по заданным параметрам "
                "поиска (день недели, номер урока, время начала "
                "и окончания)",
    parameters=FunctionParameters(
        type="object",
        properties={
            "day_of_weeks": FunctionParametersProperty(
                type="array",
                items={"type": "integer"},
                description="Дни недели для фильтрации "
                           "(1 - понедельник, 7 - воскресенье)"
            ),
            "lesson_numbers": FunctionParametersProperty(
                type="array",
                items={"type": "integer"},
                description="Номера уроков для фильтрации (от 0 до 24, "
                           "где 0 - классный час/внеурочная деятельность)"
            ),
            "start_time_ge": FunctionParametersProperty(
                type="string",
                description="Время начала урока от (включительно). "
                           "Формат: ЧЧ:ММ"
            ),
            "start_time_le": FunctionParametersProperty(
                type="string",
                description="Время начала урока до (включительно). "
                           "Формат: ЧЧ:ММ"
            ),
            "end_time_ge": FunctionParametersProperty(
                type="string",
                description="Время окончания урока от (включительно). "
                           "Формат: ЧЧ:ММ"
            ),
            "end_time_le": FunctionParametersProperty(
                type="string",
                description="Время окончания урока до (включительно). "
                           "Формат: ЧЧ:ММ"
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
                              "(например, 'Найдено 12 записей')"
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "day_of_week": {
                            "type": "integer",
                            "description": "День недели "
                                          "(1-7, где 1 - понедельник)"
                        },
                        "lesson_number": {
                            "type": "integer",
                            "description": "Номер урока по порядку "
                                          "(0 - классный час/внеурочная "
                                          "деятельность, "
                                          "1-12 - основные уроки)"
                        },
                        "start_time": {
                            "type": "string",
                            "format": "time",
                            "description": "Время начала урока "
                                          "в формате ЧЧ:ММ:СС"
                        },
                        "end_time": {
                            "type": "string",
                            "format": "time",
                            "description": "Время окончания урока "
                                          "в формате ЧЧ:ММ:СС"
                        }
                    }
                },
                "description": "Список записей расписания звонков, "
                              "соответствующих критериям поиска"
            }
        }
    }
)

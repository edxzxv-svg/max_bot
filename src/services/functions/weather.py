WEATHER_FORECAST = {
    "name": "weather_forecast",
    "description": "Возвращает температуру на заданный период",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "Местоположение, например, название города"
            },
            "format": {
                "type": "string",
                "enum": [
                    "celsius",
                    "fahrenheit"
                ],
                "description": "Единицы измерения температуры"
            },
            "num_days": {
                "type": "integer",
                "description": "Период, для которого нужно вернуть"
            }
        },
        "required": [
            "location",
            "num_days"
        ]
    },
    "return_parameters": {
        "type": "object",
        "properties": {
            "status": {
                "description": "Статус",
                "enum": [
                    "success",
                    "fail"
                ],
                "type": "string"
            },
            "location": {
                "type": "string",
                "description": "Местоположение, например, название города"
            },
            "temperature": {
                "type": "integer",
                "description": "Температура для заданного местоположения"
            },
            "forecast": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Описание погодных условий"
            },
            "error": {
                "type": "string",
                "description": "Возвращается при возникновении ошибки. Содержит описание ошибки"
            }
        }
    }
}
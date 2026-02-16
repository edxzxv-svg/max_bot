import aiohttp
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class WeatherService:
    """Сервис для получения погоды с бесплатного Open-Meteo API"""

    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    async def get_forecast(self, location: str, num_days: int = 1, format: str = "celsius") -> dict:
        """
        Получение прогноза погоды через Open-Meteo

        Args:
            location: Название города
            num_days: Количество дней прогноза
            format: celsius или fahrenheit

        Returns:
            dict в формате, соответствующем return_parameters
        """
        try:
            # Шаг 1: Получаем координаты города (геокодинг)
            coordinates = await self._get_coordinates(location)
            if not coordinates:
                return {
                    "status": "fail",
                    "error": f"Город '{location}' не найден"
                }

            lat, lon = coordinates

            # Шаг 2: Получаем погоду по координатам
            weather_data = await self._fetch_weather(lat, lon, num_days)

            # Шаг 3: Формируем ответ в нужном формате
            return self._format_response(
                location=location,
                weather_data=weather_data,
                num_days=num_days,
                format=format
            )

        except Exception as e:
            logger.error(f"Error getting weather: {e}")
            return {
                "status": "fail",
                "error": str(e)
            }

    async def _get_coordinates(self, location: str) -> tuple | None:
        """
        Геокодинг - получение координат по названию города
        Используем бесплатный Open-Meteo Geocoding API
        """
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": location,
            "count": 1,
            "language": "ru",
            "format": "json"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("results"):
                            result = data["results"][0]
                            logger.info(
                                f"Found coordinates for {location}: ({result['latitude']}, {result['longitude']})")
                            return (result["latitude"], result["longitude"])
                    else:
                        logger.error(f"Geocoding error: {response.status}")
            except Exception as e:
                logger.error(f"Geocoding request failed: {e}")

        return None

    async def _fetch_weather(self, lat: float, lon: float, num_days: int) -> dict:
        """
        Получение погоды с Open-Meteo API
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "temperature_2m_min", "weathercode", "precipitation_sum"],
            "timezone": "auto",
            "forecast_days": num_days
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Weather API error: {response.status}")
                        return {}
            except Exception as e:
                logger.error(f"Weather request failed: {e}")
                return {}

    def _format_response(self, location: str, weather_data: dict, num_days: int, format: str) -> dict:
        """
        Форматирование ответа в соответствии с return_parameters
        """
        if not weather_data or "daily" not in weather_data:
            return {
                "status": "fail",
                "error": "Не удалось получить данные о погоде"
            }

        daily = weather_data["daily"]

        # Преобразуем код погоды в текстовое описание
        weather_codes = {
            0: "Ясно",
            1: "Преимущественно ясно",
            2: "Переменная облачность",
            3: "Пасмурно",
            45: "Туман",
            48: "Изморозь",
            51: "Легкая морось",
            53: "Морось",
            55: "Сильная морось",
            61: "Небольшой дождь",
            63: "Дождь",
            65: "Сильный дождь",
            71: "Небольшой снег",
            73: "Снег",
            75: "Сильный снег",
            77: "Снежная крупа",
            80: "Ливневый дождь",
            81: "Сильный ливень",
            82: "Шквал",
            85: "Снегопад",
            86: "Сильный снегопад",
            95: "Гроза"
        }

        # Получаем температуру (конвертируем если нужно)
        temp_max = daily["temperature_2m_max"][0]
        if format == "fahrenheit":
            temp_max = temp_max * 9 / 5 + 32

        # Формируем прогноз
        forecast = []
        for i in range(min(num_days, len(daily["time"]))):
            date = datetime.fromisoformat(daily["time"][i]).strftime("%d.%m")
            weather_code = daily["weathercode"][i]
            description = weather_codes.get(weather_code, "Неизвестно")
            temp_max_day = daily["temperature_2m_max"][i]
            temp_min_day = daily["temperature_2m_min"][i]

            if format == "fahrenheit":
                temp_max_day = temp_max_day * 9 / 5 + 32
                temp_min_day = temp_min_day * 9 / 5 + 32

            forecast.append(
                f"{date}: {description}, {temp_max_day:.0f}°/{temp_min_day:.0f}°"
            )

        return {
            "status": "success",
            "location": location,
            "temperature": int(round(temp_max)),  # integer как в return_parameters
            "forecast": forecast
        }


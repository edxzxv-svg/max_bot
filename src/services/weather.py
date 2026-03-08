import logging
from datetime import datetime
from http import HTTPStatus
from typing import Any, cast

import aiohttp

logger = logging.getLogger(__name__)


class WeatherService:
    """Сервис для получения погоды с бесплатного Open-Meteo API."""

    def __init__(self) -> None:
        self.get_forecast_url = "https://api.open-meteo.com/v1/forecast"
        self.get_coord_url = "https://geocoding-api.open-meteo.com/v1/search"

    async def get_forecast(
            self, location: str,
            num_days: int = 1,
            format_str: str = "celsius"
    ) -> dict[str, Any]:
        """Получение прогноза погоды через Open-Meteo.

        Args:
            location: Название города
            num_days: Количество дней прогноза
            format_str: celsius или fahrenheit

        Returns:
            dict в формате, соответствующем return_parameters
        """
        try:
            coordinates = await self._get_coordinates(location)
            if not coordinates:
                return {
                    "status": "fail",
                    "error": f"Город '{location}' не найден"
                }

            lat, lon = coordinates
            weather_data = await self._fetch_weather(lat, lon, num_days)

            return self._format_response(
                location=location,
                weather_data=weather_data,
                num_days=num_days,
                format_str=format_str
            )

        except Exception as e:
            logger.exception("Error getting weather")
            return {
                "status": "fail",
                "error": str(e)
            }

    async def _get_coordinates(
            self,
            location: str
    ) -> tuple[float, float] | None:
        """Геокодинг - получение координат по названию города.

        Используем бесплатный Open-Meteo Geocoding API для преобразования
        названия города в географические координаты (широта, долгота).
        """
        params: dict[str, Any] = {
            "name": location,
            "count": 1,
            "language": "ru",
            "format": "json"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                        self.get_coord_url,
                        params=params,
                ) as response:
                    if response.status == HTTPStatus.OK:
                        data = await response.json()
                        if data.get("results"):
                            result = data["results"][0]
                            logger.info(
                                "Found coordinates for %s: (%s, %s)",
                                location,
                                result["latitude"],
                                result["longitude"]
                            )
                            return (result["latitude"], result["longitude"])
                    else:
                        logger.error("Geocoding error: %s", response.status)
            except Exception:
                logger.exception("Geocoding request failed")

        return None

    async def _fetch_weather(
            self,
            lat:
            float,
            lon: float,
            num_days: int,
    ) -> dict[str, Any]:
        """Получение погоды с Open-Meteo API."""
        params: dict[str, Any] = {
            "latitude": lat,
            "longitude": lon,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "weathercode",
                "precipitation_sum"
            ],
            "timezone": "auto",
            "forecast_days": num_days
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                        self.get_forecast_url,
                        params=params
                ) as response:
                    if response.status == HTTPStatus.OK:
                        data = await response.json()
                        return cast(dict[Any, Any], data)

                    logger.exception("Weather API error")
                    return {}
            except Exception:
                logger.exception ("Weather request failed")
                return {}

    def _format_response(
            self,
            location: str,
            weather_data: dict[str, Any],
            num_days: int,
            format_str: str
    ) -> dict[str, Any]:

        if not weather_data or "daily" not in weather_data:
            return {
                "status": "fail",
                "error": "Не удалось получить данные о погоде"
            }

        daily = weather_data["daily"]

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
        if format_str == "fahrenheit":
            temp_max = temp_max * 9 / 5 + 32

        forecast = []
        for i in range(min(num_days, len(daily["time"]))):
            date = datetime.fromisoformat(daily["time"][i]).strftime("%d.%m")
            weather_code = daily["weathercode"][i]
            description = weather_codes.get(weather_code, "Неизвестно")
            t_max_day = daily["temperature_2m_max"][i]
            t_min_day = daily["temperature_2m_min"][i]

            if format_str == "fahrenheit":
                t_max_day = t_max_day * 9 / 5 + 32
                t_min_day = t_min_day * 9 / 5 + 32

            forecast.append(
                f"{date}: {description}, {t_max_day:.0f}°/{t_min_day:.0f}°"
            )

        return {
            "status": "success",
            "location": location,
            "temperature": int(round(temp_max)),
            "forecast": forecast
        }

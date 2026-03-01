from datetime import UTC, datetime
from typing import Any

from pydub import AudioSegment
import aiohttp
import tempfile, os
from gigachat import Chat, GigaChat, Messages, MessagesRole, FunctionCall
from gigachat.models import Storage
from maxapi import Bot
from maxapi.enums.parse_mode import ParseMode
from maxapi.types import MessageCreated, ButtonsPayload
import json
import speech_recognition as sr
from speech_recognition import UnknownValueError

from commands import UserListCommand, BaseCommand
from dependes import (
    get_student_service, get_weather_service, get_user_repository, get_teacher_service, get_schedule_service,
    get_call_service, get_student_repository, get_teacher_repository
)
from emums.prompts import AgentProfile
from models import User, Student, Teacher
from schemes.request import StudentListRequest, TeacherListRequest, ScheduleRequest, CallRequest
from services.functions import WEATHER_FORECAST_FUNCTION, TEACHER_LIST_FUNCTION, SCHEDULE_FUNCTION
from services.functions import STUDENT_LIST_FUNCTION, CALL_LIST_FUNCTION
from src.emums.persons import UserRole, UserStatus
from src.session import async_session_maker
from src.settings import settings
import logging

MAX_MESSAGE_LENGTH = 2048
BASE_URL_FILES = "https://platform-api.max.ru/v1/files"

logger = logging.getLogger(__name__)


class MaxBot(Bot):
    def __init__(
            self,
            token: str,
            stream: bool = False
    ):
        super().__init__(token)
        self.access_token = token
        self.user_repo = get_user_repository()
        self.student_repo = get_student_repository()
        self.teacher_repo = get_teacher_repository()
        self.parse_mode = ParseMode.MARKDOWN
        self.stream = stream
        self.thread_ids: dict[int, int] = {}
        self.weather_service =get_weather_service()
        self.student_service = get_student_service()
        self.teacher_service = get_teacher_service()
        self.schedule_service = get_schedule_service()
        self.call_service = get_call_service()
        self.admin_commands: list[BaseCommand] = [
            UserListCommand(self.user_repo)
        ]
        self.recognizer = sr.Recognizer()

    async def handle_message_created(
            self,
            event: MessageCreated,
    ) -> None:
        if self.stream:
            await self.stream_handle_message_created(event)
            return

        chat_id, user_id = event.get_ids()
        user, profile = await self.get_user_profile(user_id)

        chat_request = await self.build_chat_request(event, user, profile)
        payload = await self.build_buttons_payload(event)

        with GigaChat(
                credentials=settings.gigachat.TOKEN,
                verify_ssl_certs=False,
        ) as giga:
            try:
                response = giga.chat(chat_request)
                message = response.choices[0].message
                if response.thread_id:
                    self.thread_ids[chat_id] = response.thread_id

                while True:
                    if message.function_call:
                        function_result = await self._execute_function(message.function_call, user)

                        function_call_received = [
                            Messages(
                                role=MessagesRole.ASSISTANT,
                                content="",
                                function_call=message.function_call
                            ),
                            Messages(
                                role=MessagesRole.FUNCTION,
                                content=json.dumps(function_result, ensure_ascii=False),
                                name=message.function_call.name
                            )
                        ]

                        chat_request.messages += function_call_received
                        # chat_request.storage.thread_id = response.thread_id

                        response = giga.chat(chat_request)
                        message = response.choices[0].message
                        continue

                    if message.content:
                        await event.message.answer(
                            message.content,
                            parse_mode=self.parse_mode,
                            attachments=[payload] if payload else None
                        )

                    break

            except Exception as e:
                logger.error(e)
                self.thread_ids.pop(chat_id)

    async def handle_attachments(
        self,
        event: MessageCreated,
    ) -> None:
        if not event.message.body.attachments:
            return

        for attach in event.message.body.attachments:
            file_name = ""
            match attach.type:
                case 'image':
                    file_name = f"{attach.payload.token[0:15]}.riff"
                    # file_name = file_name.replace("/", "_")
                case 'file':
                    file_name = attach.filename
                case 'video':
                    file_name = f"{attach.payload.token[0:15]}.mp4"
                case 'audio':
                    if text := await self.parse_audio(
                        url=attach.payload.url,
                        token=attach.payload.token,
                    ):
                        event.message.body.text = text
                        await self.handle_message_created(event)
                case _:
                    logger.error(f"Unknown attachment type: {attach.type}")
                    return

    async def parse_audio(
            self,
            token: str,
            url: str,
            language="ru-RU"
    ) -> str | None:
        headers = {"Authorization": f"Bearer {self.access_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Error of download audio: {response.status}")
                    return None

                audio_bytes = await response.read()

                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as mp3_file:
                    mp3_file.write(audio_bytes)
                    mp3_path = mp3_file.name

                wav_path = mp3_path.replace('.mp3', '.wav')

                try:
                    # Конвертируем аудио
                    audio = AudioSegment.from_mp3(mp3_path)
                    audio = audio.set_channels(1)
                    audio = audio.set_frame_rate(16000)
                    audio = audio.apply_gain(-audio.dBFS)
                    audio.export(wav_path, format="wav")

                    # Распознаём речь
                    with sr.AudioFile(wav_path) as source:
                        audio_data = self.recognizer.record(source)

                        try:
                            text = self.recognizer.recognize_google(
                                audio_data,
                                language=language  # Добавил language
                            )
                            logger.info(f"Распознанный текст: {text}")
                            return text

                        except sr.UnknownValueError:
                            logger.error("Google Speech Recognition не смог распознать аудио")
                            return None

                        except sr.RequestError as e:
                            logger.error(f"Ошибка запроса к Google Speech Recognition: {e}")
                            return None

                except Exception as e:
                    logger.error(f"Ошибка обработки аудио: {e}")
                    return None

                finally:
                    # Удаляем временные файлы
                    for path in [mp3_path, wav_path]:
                        if os.path.exists(path):
                            try:
                                os.unlink(path)
                            except:
                                pass


    async def stream_handle_message_created(
            self,
            event: MessageCreated,
    ) -> None:
        chat_id, user_id = event.get_ids()
        user, profiler = await self.get_user_profile(user_id)
        chat_request = await self.build_chat_request(event, user, profiler)
        payload = await self.build_buttons_payload(event)

        with GigaChat(
                credentials=settings.gigachat.TOKEN,
                verify_ssl_certs=False,
        ) as giga:
            try:
                function_call_received = []
                while True:
                    buff = ""
                    for chunk in giga.stream(chat_request):
                        if hasattr(chunk, 'storage') and hasattr(chunk.storage, 'thread_id'):
                            self.thread_ids[chat_id] = chunk.storage.thread_id

                        message = chunk.choices[0].delta
                        if message.function_call:
                            function_result = await self._execute_function(message.function_call, user)
                            function_call_received.append(message)
                            function_call_received.append(
                                Messages(
                                    role=MessagesRole.FUNCTION,
                                    content=json.dumps(function_result, ensure_ascii=False),
                                    name=message.function_call.name
                                )
                            )
                            continue

                        if message.content:
                            if len(buff) + len(message.content) > MAX_MESSAGE_LENGTH:
                                await event.message.answer(buff, parse_mode=self.parse_mode)
                                buff = message.content
                            else:
                                buff += message.content

                    if buff:
                        await event.message.answer(buff, parse_mode=self.parse_mode,
                                                   attachments=[payload] if payload else None)

                    if function_call_received:
                        chat_request = Chat(
                            stream=True,
                            messages=function_call_received.copy(),
                            storage=chat_request.storage,
                        )
                        function_call_received.clear()
                    else:
                        break
            except Exception as e:
                logger.error(e)
                self.thread_ids.pop(chat_id)

        # await self.set_history(chat_id, chat_request.messages)

    async def build_chat_request(
            self,
            event: MessageCreated,
            user: User,
            profile: Student | Teacher | None = None,
    ) -> Chat:
        max_tokens: int | None = 200
        model = "GigaChat"
        chat_id, _ = event.get_ids()
        thread_id = None

        if not thread_id:
            self.thread_ids.get(chat_id)

        storage = Storage(
            is_stateful=True,
            thread_id=thread_id,
            metadata={
                "chat_id": str(chat_id),
                "user_id": str(user.user_id),
                "role": user.role
            },

        )

        if user.role == UserRole.ADMIN:
            model = "GigaChat-MAX"
            max_tokens = 1000
        elif user.role == UserRole.TEACHER:
            model = "GigaChat-Pro"
            max_tokens = None
        elif user.role == UserRole.STUDENT:
            max_tokens = 500

        messages = []
        content = await self.build_system_prompt(
            AgentProfile.SCHOOL_ASSISTANT_PROMPT_2,
            user=user,
            profile=profile,
        )

        if not thread_id:
            messages.append(
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=content
                ),
            )

        messages.append(
            Messages(
                role=MessagesRole.USER,
                content=event.message.body.text,
            ),
        )

        functions = [
            WEATHER_FORECAST_FUNCTION,
        ]

        match user.role:
            case UserRole.ADMIN:
                functions += [
                    STUDENT_LIST_FUNCTION,
                    TEACHER_LIST_FUNCTION,
                    SCHEDULE_FUNCTION,
                    CALL_LIST_FUNCTION,
                ]
            case UserRole.TEACHER:
                functions += [
                    STUDENT_LIST_FUNCTION,
                    TEACHER_LIST_FUNCTION,
                    SCHEDULE_FUNCTION,
                    CALL_LIST_FUNCTION,
                ]
            case UserRole.STUDENT:
                functions += [
                    STUDENT_LIST_FUNCTION,
                    SCHEDULE_FUNCTION,
                    CALL_LIST_FUNCTION,
                ]

        chat_request = Chat(
            stream=self.stream,
            model=model if not thread_id else None,
            messages=messages,
            max_tokens=max_tokens,
            storage=storage,
            functions=functions,
            function_call="auto",
        )
        return chat_request

    async def build_system_prompt(
            self,
            base_prompt: str,
            user: User,
            profile: Student | Teacher | None = None,
    ) -> str:
        prompt_items = [
            base_prompt,
            f"В ответах пользователю используй разметку {self.parse_mode}",
        ]

        user_profile: dict [str, str | int] = {'role': user.role}
        if user.name:
            user_profile['name'] = user.name

        if profile:
            user_profile['last_name'] = profile.last_name
            user_profile['first_name'] = profile.first_name
            user_profile['second_name'] = profile.second_name
            user_profile['birth_day'] = profile.birth_day.isoformat()

            if isinstance(profile, Student):
                user_profile['class_number'] = profile.class_number
                user_profile['class_parallel'] = profile.class_parallel


        prompt_items.append(f"Информация о собеседнике: user={user_profile}")
        return ";\n".join(prompt_items)

    async def build_buttons_payload(self, event: MessageCreated) -> ButtonsPayload | None:
        payload = None
        # buttons: list[ButtonsPayload] = []
        return payload

    async def get_user_profile(self, user_id: int) -> tuple[User, Student | Teacher | None] | None:
        async with async_session_maker() as session:
            user = await self.user_repo.get_by(session, user_id=user_id)
            if not user:
                user = await self.user_repo.create(
                    session,
                    user_id=user_id,
                    role=UserRole.GUEST,
                    status=UserStatus.ACTIVE,
                )
            else:
                await self.user_repo.update(
                    session, user, last_update_date=datetime.now(UTC)
                )

            if user:
                student = await self.student_repo.get_by(session, user_uuid=user.uuid)
                teacher = await self.teacher_repo.get_by(session, user_uuid=user.uuid)

            return user, student or teacher

    async def _execute_function(self, function_call: FunctionCall, user: User) -> dict[str, Any]:
        """Выполнение функции с учетом return_parameters"""
        try:
            logger.info(f"Executing function: {function_call.name}")
            logger.info(f"Arguments: {function_call.arguments}")

            match function_call.name:
                case "weather_forecast":
                    args = function_call.arguments

                    # Вызываем реальный погодный сервис
                    return await self.weather_service.get_forecast(
                        location=args.get('location', 'Москва'),
                        num_days=args.get('num_days', 1),
                        format=args.get('format', 'celsius')
                    )
                case "get_student_list":
                    args = function_call.arguments
                    result = await self.student_service.get_list(
                        params=StudentListRequest.model_validate(args),
                        user=user,
                    )
                    return result.model_dump(mode='json')
                case "get_teacher_list":
                    args = function_call.arguments
                    result = await self.teacher_service.get_list(
                        params=TeacherListRequest.model_validate(args),
                        user=user,
                    )
                    return result.model_dump(mode='json')
                case "get_schedule":
                    args = function_call.arguments
                    result = await self.schedule_service.get_list(
                        params=ScheduleRequest.model_validate(args),
                        user=user,
                    )
                    return result.model_dump(mode='json')
                case "get_calls":
                    args = function_call.arguments
                    result = await self.call_service.get_list(
                        params=CallRequest.model_validate(args),
                        user=user,
                    )
                    return result.model_dump(mode='json')
                case _:
                    return {
                        "status": "fail",
                        "error": f"Function {function_call.name} not implemented"
                    }
        except Exception as e:
            logger.error(f"Error executing function: {e}")
            return {
                "status": "fail",
                "error": str(e)
            }
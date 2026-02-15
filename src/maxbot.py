from datetime import UTC, datetime
from typing import Any

from gigachat import Chat, GigaChat, Messages, MessagesRole, FunctionCall
from gigachat.models import Storage
from maxapi import Bot
from maxapi.enums.parse_mode import ParseMode
from maxapi.types import MessageCreated, ButtonsPayload
import json

from commands import UserListCommand, BaseCommand
from emums.prompts import AgentProfile
from models import User
from services import WeatherService
from services.functions import WEATHER_FORECAST
from src.emums.persons import UserRole, UserStatus
from src.repositories.user import UserRepository
from src.session import async_session_maker
from src.settings import settings
import logging

MAX_MESSAGE_LENGTH = 2048

logger = logging.getLogger(__name__)


class MaxBot(Bot):
    def __init__(self, token: str, stream: bool = False):
        super().__init__(token)
        self.user_repo = UserRepository()
        self.parse_mode = ParseMode.MARKDOWN
        self.stream = stream
        self.thread_ids: dict[int, int] = {}
        self.weather_service = WeatherService()
        self.admin_commands: list[BaseCommand] = [
            UserListCommand(self.user_repo)
        ]

    async def handle_message_created(
            self,
            event: MessageCreated,
    ) -> None:
        if self.stream:
            await self.stream_handle_message_created(event)
            return

        chat_id, user_id = event.get_ids()
        user = await self.get_user(user_id)
        chat_request = await self.build_chat_request(event, user)
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

    async def stream_handle_message_created(
            self,
            event: MessageCreated,
    ) -> None:
        chat_id, user_id = event.get_ids()
        user = await self.get_user(user_id)
        chat_request = await self.build_chat_request(event, user)
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
        content = await self.build_system_prompt(AgentProfile.SCHOOL_ASSISTANT_PROMPT_2, user)

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
            WEATHER_FORECAST
        ]

        if user.role == UserRole.ADMIN:
            functions += [
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
    ) -> str:
        prompt_items = [
            base_prompt,
            f"В ответах пользователю используй разметку {self.parse_mode}",
        ]

        user_profile = {'role': user.role}
        if user.name:
            user_profile['name'] = user.name

        prompt_items.append(f"Информация о собеседнике: {user_profile}")
        return ";\n".join(prompt_items)

    async def build_buttons_payload(self, event: MessageCreated) -> ButtonsPayload | None:
        payload = None
        # buttons: list[ButtonsPayload] = []
        return payload

    async def get_user(self, user_id: int) -> User:
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

            return user

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
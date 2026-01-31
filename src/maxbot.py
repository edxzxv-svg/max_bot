from datetime import UTC, datetime

from gigachat import Chat, GigaChat, Messages, MessagesRole
from gigachat.models import Storage
from maxapi import Bot
from maxapi.enums.parse_mode import ParseMode
from maxapi.types import MessageCreated, ButtonsPayload
from pyexpat.errors import messages

from models import User
from src.emums.persons import UserRole, UserStatus
from src.emums.prompts import AgentProfile
from src.repositories.user import UserRepository
from src.session import async_session_maker
from src.settings import settings

MAX_MESSAGE_LENGTH = 2048

class MaxBot(Bot):
    def __init__(self, token: str, stream: bool = False):
        super().__init__(token)
        self.user_repo = UserRepository()
        self.parse_mode = ParseMode.MARKDOWN
        self.stream = stream
        self.thread_ids: dict[int, int] = {}

    async def handle_message_created(
        self,
        event: MessageCreated,
    ) -> None:

        chat_id, user_id = event.get_ids()
        user = await self.get_user(user_id)
        chat_request = await self.build_chat_request(event, user)
        payload = await self.build_buttons_payload(event)

        with GigaChat(
            credentials=settings.gigachat.TOKEN, verify_ssl_certs=False
        ) as giga:
            if self.stream:
                buff = ""
                for chunk in giga.stream(chat_request):
                    if hasattr(chunk, 'storage') and hasattr(chunk.storage, 'thread_id'):
                        self.thread_ids[chat_id] = chunk.storage.thread_id
                    msg = chunk.choices[0].delta.content
                    if not msg:
                        continue
                    if len(buff) + len(msg) > MAX_MESSAGE_LENGTH:
                        await event.message.answer(
                            buff, parse_mode=self.parse_mode
                        )
                        buff = msg
                    else:
                        buff += msg
                await event.message.answer(
                    buff,
                    parse_mode=self.parse_mode,
                    attachments=[payload] if payload else None,
                )
            else:
                response = giga.chat(chat_request)
                if hasattr(response, 'thread_id'):
                    self.thread_ids[chat_id] = response.thread_id
                await event.message.answer(
                    response.choices[0].message.content,
                    parse_mode=self.parse_mode,
                    attachments=[payload] if payload else None,
                )

    async def build_chat_request(
        self,
        event: MessageCreated,
        user: User
    ) -> Chat:
        max_tokens: int | None = 200
        model = "GigaChat"
        chat_id, _ = event.get_ids()
        thread_id = self.thread_ids.get(chat_id)

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

        messages: list[Messages] = []

        if not thread_id:
            messages.append(
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=self.build_system_prompt(AgentProfile.SCHOOL_ASSISTANT_PROMPT_2, user)
                ),
            )

        messages.append(
            Messages(
                role=MessagesRole.USER,
                content=event.message.body.text,
            ),
        )

        chat_request = Chat(
            stream=self.stream,
            model=model if not thread_id else None,
            messages=messages,
            max_tokens=max_tokens,
            storage=storage,
        )
        return chat_request

    def build_system_prompt(
        self,
        base_prompt: str,
        user: User,
    ) -> str:
        prompt_items = [
            base_prompt,
            f"Используй в ответах разметку {self.parse_mode}",
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

    async def get_user(self,  user_id: int) -> User:
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
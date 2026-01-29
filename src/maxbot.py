from datetime import datetime

from gigachat.models import Storage
from maxapi import Bot
from maxapi.enums.parse_mode import ParseMode
from maxapi.types import MessageCreated, ButtonsPayload
from gigachat import GigaChat, Chat, Messages, MessagesRole

from src.emums.persons import UserRole, UserStatus
from src.emums.prompts import AgentProfile
from src.repositories.user import UserRepository
from src.session import async_session_maker
from src.settings import settings
from maxapi.types.attachments.buttons import CallbackButton, RequestContactButton

class MaxBot(Bot):
    def __init__(self, token: str):
        super().__init__(token)
        self.user_repo = UserRepository()
        self.parse_mode = ParseMode.MARKDOWN

    async def handle_message_created(self, event: MessageCreated):
        chat_id, user_id = event.get_ids()

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
                await self.user_repo.update(session, user, last_update_date=datetime.now())

        stream = False
        model = "GigaChat"
        max_tokens = 200
        storage = None
        payload = None
        buttons = []

        if user.role == UserRole.ADMIN:
            stream = True
            model = "GigaChat-MAX"
            max_tokens = 1000
            storage = Storage(
                is_stateful=True,
                metadata={
                    "user_id": chat_id,
                },
            )
            # buttons = [
            #     [RequestContactButton(text="Callback", payload="data")]
            # ]

        elif user.role == UserRole.TEACHER:
            stream = True
            model = "GigaChat-Pro"
            max_tokens = None
            storage = Storage(
                is_stateful=True,
                limit=20,
                metadata={
                    "user_id": chat_id,
                },
            )
        elif user.role == UserRole.STUDENT:
            model = "GigaChat"
            max_tokens = 500
            storage = Storage(
                is_stateful=True,
                limit=5,
                metadata={
                    "user_id": chat_id,
                },
            )

        if buttons:
            payload = ButtonsPayload(buttons=buttons).pack()

        chat_request = Chat(
            stream = stream,
            model = model,
            messages = [
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=AgentProfile.SCHOOL_ASSISTANT_PROMPT_2 + f"\n Используй в ответах разметку {self.parse_mode}",
                ),
                Messages(
                    role=MessagesRole.USER,
                    content=event.message.body.text,
                )
            ],
            max_tokens = max_tokens,
            storage = storage,
        )

        with GigaChat(credentials=settings.gigachat.TOKEN, verify_ssl_certs=False) as giga:
            if stream:
                buff = ""
                for chunk in giga.stream(chat_request):
                    msg = chunk.choices[0].delta.content
                    if len(buff) + len(msg) > 2048:
                        await event.message.answer(buff, parse_mode=self.parse_mode)
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
                await event.message.answer(
                    response.choices[0].message.content,
                    parse_mode=self.parse_mode,
                    attachments = [payload] if payload else None,
                )
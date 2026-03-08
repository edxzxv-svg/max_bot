import asyncio
import logging

from maxapi import Dispatcher, F
from maxapi.types import MessageCreated

from src.dependes import setup_dependencies
from src.maxbot import MaxBot
from src.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

setup_dependencies()
bot = MaxBot(settings.max.TOKEN, stream=False)
dp = Dispatcher()


@dp.message_created(F.message.body.text)   # type: ignore[untyped-decorator]
async def handle_message_created(event: MessageCreated) -> None:
    await bot.handle_message_created(event)

@dp.message_created(F.message.body.attachments)   # type: ignore[untyped-decorator]
async def handle_attachments(event: MessageCreated) -> None:
    await bot.handle_attachments(event)

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

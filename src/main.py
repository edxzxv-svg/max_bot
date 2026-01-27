import asyncio
import logging
from maxapi import Dispatcher, F
from maxapi.types import MessageCreated

from src.maxbot import MaxBot
from src.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = MaxBot(settings.max.TOKEN)
dp = Dispatcher()

@dp.message_created(F.message.body.text)
async def handle_message_created(event: MessageCreated):
    await bot.handle_message_created(event)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
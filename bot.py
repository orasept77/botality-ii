import logging
import asyncio

from aiogram import Bot, Dispatcher, types, html
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from config_reader import config
from middleware import ChatActionMiddleware, AccessMiddleware, CooldownMiddleware, MediaGroupMiddleware
from taskiq import InMemoryBroker

from modules.sd import StableDiffusionModule
from modules.tts import TextToSpeechModule
from modules.admin import AdminModule
from modules.llm import LargeLanguageModel


logger = logging.getLogger(__name__)
broker = InMemoryBroker()

dp = Dispatcher()
dp.message.middleware(AccessMiddleware())
dp.message.middleware(ChatActionMiddleware())
dp.message.middleware(CooldownMiddleware())
dp.message.middleware(MediaGroupMiddleware())


bot = None
                    
def initialize(dp, bot):
    available_modules = {
        "sd": StableDiffusionModule,
        "tts": TextToSpeechModule,
        "admin": AdminModule,
        "llm": LargeLanguageModel
    }
    for module in config.active_modules:
        if module in available_modules:
            available_modules[module](dp, bot, broker)


def main() -> None:
    global bot
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',)
    initialize(dp, bot)
    print('running')
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
from telethon import TelegramClient

from src.config.config import SETTINGS

bot = TelegramClient(
    session=SETTINGS.SESSION_NAME,
    api_id=SETTINGS.API_ID,
    api_hash=SETTINGS.API_HASH
)

async def startClient():
    await bot.start(bot_token=SETTINGS.BOT_TOKEN)

async def stopClient():
    await bot.disconnect()

async def getClient():
    return bot
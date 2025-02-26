from telethon import events
from datetime import datetime
import pytz

from src.utils.keyboards import start_key
from src.database.models import User
from src.config.config import TEXTS

async def init(bot):
    @bot.on(events.NewMessage(func=lambda e: e.is_private))
    async def datetime_subscription(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)

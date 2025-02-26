from telethon import events
from datetime import datetime

from src.config.config import TEXTS, SETTINGS
from src.utils.keyboards import support
from src.database.models import User

async def init(bot):
    @bot.on(events.NewMessage(func=lambda e: e.is_private))
    async def datetime_subscription(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)

        if user_data.datetime_subscription.timestamp() < datetime.now().timestamp() and user.id != SETTINGS.OWNER:
            await event.reply(TEXTS['need_subscription'][user_data.language], buttons = support())
            raise events.StopPropagation()

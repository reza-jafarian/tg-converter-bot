from telethon import events

from src.utils.keyboards import start_key, account_functions_key
from src.utils.functions import check_step
from src.database.models import User
from src.config.config import TEXTS

async def init(bot):
    @bot.on(events.NewMessage(pattern=r'^(/start|/back|🔙 back)$', func=lambda e: e.is_private))
    async def start(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)
        
        if check_step(step=user_data.step) or user_data.step == 'select':
            User.update(step='none').where(User.user_id == user.id).execute()
            button, key = start_key(), 'start'
        elif user_data.step in ['manage_functions', 'manage_profile']:
            User.update(step='select').where(User.user_id == user.id).execute()
            button, key = account_functions_key(), 'select'
        else:
            User.update(step='none').where(User.user_id == user.id).execute()
            button, key = start_key(), 'start'
        
        await event.reply(TEXTS[key][user_data.language], buttons = button)
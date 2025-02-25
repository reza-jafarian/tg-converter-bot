from telethon import events

from src.utils.keyboards import account_functions_key, functions_key, profile_key
from src.database.models import User
from src.config.config import TEXTS

async def init(bot):
    @bot.on(events.NewMessage(pattern=r'^(• Account / Profile Functions)$', func=lambda e: e.is_private))
    async def select(event):
        user = await event.get_sender()
        
        user_data, _ = User.get_or_create(user_id=user.id)
        User.update(step='select').where(User.user_id == user.id).execute()
        
        await event.reply(TEXTS['select'][user_data.language], buttons = account_functions_key())
    
    @bot.on(events.NewMessage(pattern=r'^(• Functions)$', func=lambda e: e.is_private))
    async def functions(event):
        user = await event.get_sender()
        
        user_data, _ = User.get_or_create(user_id=user.id)
        User.update(step='manage_functions').where(User.user_id == user.id).execute()
        
        await event.reply(TEXTS['select'][user_data.language], buttons = functions_key())
    
    @bot.on(events.NewMessage(pattern=r'^(• Profile)$', func=lambda e: e.is_private))
    async def profile(event):
        user = await event.get_sender()
        
        user_data, _ = User.get_or_create(user_id=user.id)
        User.update(step='manage_profile').where(User.user_id == user.id).execute()
        
        await event.reply(TEXTS['select'][user_data.language], buttons = profile_key())
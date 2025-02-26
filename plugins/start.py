from telethon import events

from src.utils.keyboards import start_key, account_functions_key, profile_key, functions_key
from src.database.models import User
from src.config.config import TEXTS

async def init(bot):
    @bot.on(events.NewMessage(pattern=r'^(/start|/back|🔙 back)$', func=lambda e: e.is_private))
    async def start(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)
        
        if user_data.step == 'select':
            User.update(step='none').where(User.user_id == user.id).execute()
            button, key = start_key(), 'start'
        
        elif user_data.step in ['manage_functions', 'manage_profile']:
            User.update(step='select').where(User.user_id == user.id).execute()
            button, key = account_functions_key(), 'select'
        
        elif user_data.step in ['update_profile_photo', 'update_name', 'update_lastname', 'update_username', 'update_bio', 'delete_lastname', 'delete_profile_photo', 'delete_username', 'delete_bio']:
            User.update(step='manage_profile').where(User.user_id == user.id).execute()
            button, key = profile_key(), 'select'
        
        elif user_data.step in ['clear_all_data', 'leave_all_channels', 'leave_all_groups', 'delete_all_chats', 'delete_all_contacts', 'join_channel_or_group', 'leave_channel_or_group']:
            User.update(step='manage_functions').where(User.user_id == user.id).execute()
            button, key = functions_key(), 'select'
        
        else:
            User.update(step='none').where(User.user_id == user.id).execute()
            button, key = start_key(), 'start'
        
        await event.reply(TEXTS[key][user_data.language], buttons = button)
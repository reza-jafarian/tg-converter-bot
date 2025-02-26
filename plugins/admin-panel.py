from telethon import events
from datetime import datetime

from src.utils.keyboards import admin_panel_key, back_to_admin_panel_key, select_ready_date
from src.utils.functions import add_time_to_now
from src.database.models import User, redis_db
from src.config.config import TEXTS, SETTINGS

async def init(bot):
    @bot.on(events.NewMessage(func=lambda e: e.is_private, chats=SETTINGS.OWNER))
    async def admin_panel(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)
        
        if event.raw_text in ['/panel', '/admin', 'amin', 'panel', '🔙 back to admin']:
            User.update(step='none').where(User.user_id == user.id).execute()
            await event.reply('<b>🤙 Hey dude, your welcome!</b>', buttons = admin_panel_key())
        
        elif event.raw_text == '📊 Bot stat':
            User.update(step='none').where(User.user_id == user.id).execute()
            await event.reply(f'<b>📊 Bot stat:\n\n👤 Persons: {User.select().count()}</b>', buttons = admin_panel_key())
        
        elif event.raw_text == '🟢 Open user':
            User.update(step='open_user').where(User.user_id == user.id).execute()
            await event.reply(f'<b>✏️ Send your person ID:</b>', buttons = back_to_admin_panel_key())
        
        elif user_data.step == 'open_user':
            if event.raw_text.isnumeric():
                if User.select().where(User.user_id == event.raw_text).exists():
                    User.update(step='send_open_date').where(User.user_id == user.id).execute()
                    redis_db.set('user_id_for_subscription', event.raw_text)
                    await event.reply('<b>🔽 Choose one of the prepared dates below or send your desired date like buttons:\n\n📚 Example: 1 hour | 1 day | 1 month | 1 year</b>', buttons = select_ready_date())
                else:
                    await event.reply(f'<b>⚠️ User [<code>{event.raw_text}</code>] not exists in the bot!</b>', buttons = back_to_admin_panel_key())
            else:
                await event.reply(f'<b>⚠️ Your sent user id is invalid!</b>', buttons = back_to_admin_panel_key())
        
        elif user_data.step == 'send_open_date':
            if event.raw_text == 'Open for test (30 minutes)':
                expire_time = add_time_to_now('30 minutes')
            else:
                expire_time = add_time_to_now(event.raw_text)
            
            target_user = redis_db.get('user_id_for_subscription').decode('utf-8')
            User.update(step='none').where(User.user_id == user.id).execute()
            User.update(datetime_subscription=expire_time).where(User.user_id == target_user).execute()
            
            await event.reply(f'<b>✅ The operation was completed successfully and the user [<code>{target_user}</code>] {event.raw_text} was added.</b>', buttons = admin_panel_key())
        
        elif event.raw_text == '🔴 Close user':
            User.update(step='close_user').where(User.user_id == user.id).execute()
            await event.reply(f'<b>✏️ Send your person ID:</b>', buttons = back_to_admin_panel_key())

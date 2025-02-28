from telethon import events
import json

from src.utils.functions import (
    get_random_device_model, get_random_app_version,
    get_random_system_version, get_json_config,
    get_random_api, get_random_profile,
)
from src.utils.keyboards import (
    update_settings_key,
    change_settings_key, back_to_json_settings_key
)
from src.database.models import User, redis_db
from src.config.config import TEXTS

async def init(bot):
    @bot.on(events.NewMessage(func=lambda e: e.is_private))
    async def auto_full(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)
        
        if user_data.step == 'change-field' and event.raw_text:
            User.update(step='none').where(User.user_id == user.id).execute()
            
            field = redis_db.get('change-field').decode('utf-8')
            redis_db.set(field, event.raw_text)
            
            await event.reply(f'<b>✅ New value successfully set for field [ <code>{field}</code> ].\n✏️ New value: <code>{event.raw_text}</code></b>', buttons = update_settings_key())
        
        else:    
            platform = 'desktop'
            if not redis_db.get('app_id'):
                redis_db.set('app_id', get_random_api(platform = platform).get('app_id'))
            if not redis_db.get('app_hash'):
                redis_db.set('app_hash', get_random_api(platform = platform).get('app_hash'))
            if not redis_db.get('device_model'):
                redis_db.set('device_model', get_random_device_model(platform = platform))
            if not redis_db.get('app_version'):
                redis_db.set('app_version', get_random_app_version(platform = platform))
            if not redis_db.get('sdk_version'):
                redis_db.set('sdk_version', get_random_system_version(platform = platform))
            if not redis_db.get('platform'):
                redis_db.set('platform', platform)
            if not redis_db.get('first_name'):
                redis_db.set('first_name', get_random_profile(name=True))
            if not redis_db.get('last_name'):
                redis_db.set('last_name', get_random_profile(lastname=True))
            if not redis_db.get('username'):
                redis_db.set('username', get_random_profile(username=True))
            if not redis_db.get('system_lang_code'):
                redis_db.set('system_lang_code', 'en-US')
            if not redis_db.get('lang_code'):
                redis_db.set('lang_code', 'en')
            if not redis_db.get('lang_pack'):
                redis_db.set('lang_pack', 'tdesktop')
            if not redis_db.get('batch_size'):
                redis_db.set('batch_size', '100')
    
    @bot.on(events.NewMessage(pattern=r'^/config$', func=lambda e: e.is_private))
    @bot.on(events.CallbackQuery(pattern=r'(back_to_json_settings|update_settings)', func=lambda e: e.is_private))
    async def config(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)
        
        User.update(step='none').where(User.user_id == user.id).execute()
        
        if hasattr(event, 'data'):
            await event.edit(
                text = f'{TEXTS["set_settings"][user_data.language]}\n\n<pre><code class="language-json">{json.dumps(get_json_config(), indent=4, ensure_ascii=False)}</code></pre>\n\n.',
                buttons = change_settings_key()    
            )
        else: 
            await event.reply(
                message = f'{TEXTS["set_settings"][user_data.language]}\n\n<pre><code class="language-json">{json.dumps(get_json_config(), indent=4, ensure_ascii=False)}</code></pre>\n\n.',
                buttons = change_settings_key()    
            )
    
    @bot.on(events.CallbackQuery(pattern=r'^(change-.*)$', func=lambda e: e.is_private))
    async def change_field(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)
        
        field = event.data.decode().split('-')[1]
        redis_db.set('change-field', field)
        User.update(step='change-field').where(User.user_id == user.id).execute()
        
        await event.edit(f'<b>⬇️ Send new value for [ {field} ]:</b>', buttons = back_to_json_settings_key())
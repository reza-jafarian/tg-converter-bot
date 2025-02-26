from telethon import events

from src.utils.functions import analysis_step
from src.utils.keyboards import back_key
from src.database.models import User
from src.config.config import TEXTS

async def init(bot):
    @bot.on(events.NewMessage(pattern='^(Check session|Check T-data|Session to json|Session to txt|Session to string|T-data to session|Session to T-data|Enable 2FA|Reset 2FA|Disable 2FA)$', func=lambda e: e.is_private))
    @bot.on(events.NewMessage(pattern='^(Update Name|Update LastName|Update UserName|Update Bio|Delete UserName|Delete LastName|Delete Bio)$', func=lambda e: e.is_private))
    @bot.on(events.NewMessage(pattern='^(Clear All Data|Leave All Channels|Leave All Groups|Delete All Chats|Delete All Contacts|Join Channel/Group|Leave Channel/Group)$', func=lambda e: e.is_private))
    async def send_zip_file(event):
        user = await event.get_sender()
        
        user_data, _ = User.get_or_create(user_id=user.id)
        User.update(step=analysis_step(text=event.raw_text)).where(User.user_id == user.id).execute()
        
        await event.reply(str(TEXTS['send_file'][user_data.language]).format(event.raw_text), buttons = back_key())
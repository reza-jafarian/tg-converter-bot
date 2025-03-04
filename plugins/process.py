from telethon import events
import asyncio
import random

from src.utils.functions import extract_sessions_zip_file, extract_tdata_zip_file, process_method, check_step
from src.utils.keyboards import start_key, back_key, finish_upload_key
from src.database.models import User, redis_db
from src.config.config import TEXTS

async def init(bot):
    @bot.on(events.NewMessage(func=lambda e: e.is_private and e.file))
    async def process(event):
        user = await event.get_sender()
        user_data, _ = User.get_or_create(user_id=user.id)
        
        if check_step(step = user_data.step):
            if event.message.media.document.mime_type == 'application/zip':
                User.update(step='processing').where(User.user_id == user.id).execute()
                wait = await event.reply(TEXTS['extracting'][user_data.language])
                
                random_uniqe_code = random.randint(111111, 999999)
                file_name = event.message.media.document.attributes[0].file_name
                await event.download_media(file_name)
                
                if user_data.step in ['check_tdata', 'tdata_to_session']:
                    extract_tdata_zip_file(zip_path = file_name, dest_folder = f'sessions/{user.id}/{random_uniqe_code}')
                else:
                    extract_sessions_zip_file(zip_path = file_name, dest_folder = f'sessions/{user.id}/{random_uniqe_code}')
                
                await wait.edit(str(TEXTS['wait'][user_data.language]).format(0, 0))
                
                response = await process_method(
                    wait = wait,
                    user_id = user.id,
                    random_uniqe_code = random_uniqe_code,
                    step = user_data.step,
                )
                
                if response[0]:
                    User.update(step='none').where(User.user_id == user.id).execute()
                    
                    await wait.delete()
                    await bot.send_message(user.id, TEXTS['help'][user_data.language])
                    await event.reply(str(TEXTS['done'][user_data.language]).format(
                            response[1].get('count', 0),
                            response[1].get('success', 0),
                            response[1].get('unsuccess', 0),
                            response[1].get('invalid', 0),
                            response[1].get('error', 0)
                        ),
                    buttons = start_key())
                
                else:
                    User.update(step='none').where(User.user_id == user.id).execute()
                    await wait.delete()
                    await event.reply(TEXTS['error'][user_data.language], buttons = start_key())
            else:
                await event.reply(TEXTS['invalid_file'][user_data.language], buttons = back_key())
    
    @bot.on(events.NewMessage(func=lambda e: e.is_private))
    @bot.on(events.CallbackQuery(pattern=r'^(finish_upload)$', func=lambda e: e.is_private))
    async def manage_texts(event):
        user = await event.get_sender()    
        user_data, _ = User.get_or_create(user_id=user.id)
        
        if hasattr(event, 'file') and user_data.step in ['enable_2fa', 'disable_2fa']:
            wait = await event.reply(TEXTS['extracting'][user_data.language])
                
            random_uniqe_code = random.randint(111111, 999999)
            file_name = event.message.media.document.attributes[0].file_name
            await event.download_media(file_name)
            extract_sessions_zip_file(zip_path = file_name, dest_folder = f'sessions/{user.id}/{random_uniqe_code}')
            
            await wait.edit(str(TEXTS['wait'][user_data.language]).format(0, 0))
            
            User.update(step=f'send_current_password-{random_uniqe_code}-{user_data.step}').where(User.user_id == user.id).execute()
            
            await wait.delete()
            await event.reply(str(TEXTS['send_current_password'][user_data.language]).format(event.raw_text), buttons = back_key())
        
        elif hasattr(event, 'file') and user_data.step in ['join_channel_or_group', 'leave_channel_or_group']:
            wait = await event.reply(TEXTS['extracting'][user_data.language])
                
            random_uniqe_code = random.randint(111111, 999999)
            file_name = event.message.media.document.attributes[0].file_name
            await event.download_media(file_name)
            extract_sessions_zip_file(zip_path = file_name, dest_folder = f'sessions/{user.id}/{random_uniqe_code}')
            
            await wait.edit(str(TEXTS['wait'][user_data.language]).format(0, 0))
            
            User.update(step=f'send_chat_username-{random_uniqe_code}-{user_data.step}').where(User.user_id == user.id).execute()
            
            await wait.delete()
            await event.reply(str(TEXTS['send_chat_username'][user_data.language]).format(event.raw_text), buttons = back_key())
        
        elif (hasattr(event, 'file') or hasattr(event, 'data')) and user_data.step == 'mix_zip_files':
            if not hasattr(event, 'data'):
                wait = await event.reply(TEXTS['extracting'][user_data.language])
                
                if redis_db.get(f'{user.id}-lastmsgidformix'):
                    try:
                        await bot.edit_message(
                            entity = user.id,
                            message = int(redis_db.get(f'{user.id}-lastmsgidformix').decode()),
                            text = TEXTS['wait_for_upload'][user_data.language]
                        )
                    except:
                        pass
                
                if not redis_db.get(f'{user.id}-mix_zip_file_code'):
                    random_uniqe_code = random.randint(111111, 999999)
                    redis_db.set(f'{user.id}-mix_zip_file_code', random_uniqe_code)
                else:
                    random_uniqe_code = redis_db.get(f'{user.id}-mix_zip_file_code').decode('utf-8')
                
                file_name = event.message.media.document.attributes[0].file_name
                await event.download_media(file_name)
                extract_sessions_zip_file(zip_path = file_name, dest_folder = f'sessions/{user.id}/{random_uniqe_code}')
            
                await wait.edit(TEXTS['extracted'][user_data.language] + '\n\n' + str(TEXTS['send_file'][user_data.language]).format('Miz Zip Files'), buttons = finish_upload_key())
                
                redis_db.set(f'{user.id}-lastmsgidformix', wait.id)
            
            elif hasattr(event, 'data') and event.data.decode() == 'finish_upload':
                await event.edit(buttons = finish_upload_key(finished=True))
                await asyncio.sleep(1)
                
                await event.delete()
                wait = await event.reply(str(TEXTS['wait'][user_data.language]).format(0, 0), buttons = back_key())
            
                random_uniqe_code = redis_db.get(f'{user.id}-mix_zip_file_code').decode()
                current_step = user_data.step
                
                User.update(step='processing').where(User.user_id == user.id).execute()
                
                response = await process_method(
                    wait = wait,
                    user_id = user.id,
                    random_uniqe_code = random_uniqe_code,
                    step = current_step,
                )
                    
                if response[0]:
                    User.update(step='none').where(User.user_id == user.id).execute()
                    
                    await wait.delete()
                    await bot.send_message(user.id, TEXTS['help'][user_data.language])
                    await event.reply(str(TEXTS['done'][user_data.language]).format(
                            response[1].get('count', 0),
                            response[1].get('success', 0),
                            response[1].get('unsuccess', 0),
                            response[1].get('invalid', 0),
                            response[1].get('error', 0)
                        ),
                    buttons = start_key())
                
                else:
                    User.update(step='none').where(User.user_id == user.id).execute()
                    await wait.delete()
                    await event.reply(TEXTS['error'][user_data.language], buttons = start_key())
        
        elif hasattr(event, 'file') and user_data.step == 'extract_zip_files':
            wait = await event.reply(TEXTS['extracting'][user_data.language])
                
            random_uniqe_code = random.randint(111111, 999999)
            file_name = event.message.media.document.attributes[0].file_name
            await event.download_media(file_name)
            extract_sessions_zip_file(zip_path = file_name, dest_folder = f'sessions/{user.id}/{random_uniqe_code}')
            
            User.update(step=f'send_count_want-{random_uniqe_code}-{user_data.step}').where(User.user_id == user.id).execute()
        
            await wait.delete()
            await event.reply(TEXTS['extracted'][user_data.language] + '\n\n' + TEXTS['send_want_count'][user_data.language], buttons = back_key())
        
        elif user_data.step.startswith('send_chat_username-'):
            wait = await event.reply(str(TEXTS['wait'][user_data.language]).format(0, 0), buttons = back_key())
            
            random_uniqe_code = user_data.step.split('-')[1]
            current_step = user_data.step.split('-')[2]
            
            User.update(step='processing').where(User.user_id == user.id).execute()
            
            response = await process_method(
                wait = wait,
                user_id = user.id,
                random_uniqe_code = random_uniqe_code,
                step = current_step,
                chat_username = event.raw_text
            )
                
            if response[0]:
                User.update(step='none').where(User.user_id == user.id).execute()
                
                await wait.delete()
                await bot.send_message(user.id, TEXTS['help'][user_data.language])
                await event.reply(str(TEXTS['done'][user_data.language]).format(
                        response[1].get('count', 0),
                        response[1].get('success', 0),
                        response[1].get('unsuccess', 0),
                        response[1].get('invalid', 0),
                        response[1].get('error', 0)
                    ),
                buttons = start_key())
            
            else:
                User.update(step='none').where(User.user_id == user.id).execute()
                await wait.delete()
                await event.reply(TEXTS['error'][user_data.language], buttons = start_key())
        
        elif user_data.step.startswith('send_current_password-'):
            wait = await event.reply(str(TEXTS['wait'][user_data.language]).format(0, 0), buttons = back_key())
            
            random_uniqe_code = user_data.step.split('-')[1]
            current_step = user_data.step.split('-')[2]
            
            if current_step == 'enable_2fa':
                User.update(step=f'send_new_password-{random_uniqe_code}').where(User.user_id == user.id).execute()
                redis_db.set(f'{user.id}-current_password', event.raw_text)
                
                await wait.delete()
                await event.reply(str(TEXTS['send_new_password'][user_data.language]).format(event.raw_text), buttons = back_key())
            else:
                User.update(step='processing').where(User.user_id == user.id).execute()
                
                response = await process_method(
                    wait = wait,
                    user_id = user.id,
                    random_uniqe_code = random_uniqe_code,
                    step = 'disable_2fa',
                    current_password = event.raw_text
                )
                    
                if response[0]:
                    User.update(step='none').where(User.user_id == user.id).execute()
                    
                    await wait.delete()
                    await bot.send_message(user.id, TEXTS['help'][user_data.language])
                    await event.reply(str(TEXTS['done'][user_data.language]).format(
                            response[1].get('count', 0),
                            response[1].get('success', 0),
                            response[1].get('unsuccess', 0),
                            response[1].get('invalid', 0),
                            response[1].get('error', 0)
                        ),
                    buttons = start_key())
                
                else:
                    User.update(step='none').where(User.user_id == user.id).execute()
                    await wait.delete()
                    await event.reply(TEXTS['error'][user_data.language], buttons = start_key())
        
        elif user_data.step.startswith('send_new_password-'):
            random_uniqe_code = user_data.step.split('-')[1]
            User.update(step='processing').where(User.user_id == user.id).execute()
            wait = await event.reply(str(TEXTS['wait'][user_data.language]).format(0, 0), buttons = back_key())
            
            response = await process_method(
                wait = wait,
                user_id = user.id,
                random_uniqe_code = random_uniqe_code,
                step = 'enable_2fa',
                current_password = redis_db.get(f'{user.id}-current_password').decode('utf-8'),
                new_password = event.raw_text,
            )
                
            if response[0]:
                User.update(step='none').where(User.user_id == user.id).execute()
                
                await wait.delete()
                await bot.send_message(user.id, TEXTS['help'][user_data.language])
                await event.reply(str(TEXTS['done'][user_data.language]).format(
                        response[1].get('count', 0),
                        response[1].get('success', 0),
                        response[1].get('unsuccess', 0),
                        response[1].get('invalid', 0),
                        response[1].get('error', 0)
                    ),
                buttons = start_key())
            
            else:
                User.update(step='none').where(User.user_id == user.id).execute()
                await wait.delete()
                await event.reply(TEXTS['error'][user_data.language], buttons = start_key())

from telethon import TelegramClient, errors, types, functions
from telethon.sessions import SQLiteSession, StringSession
from phonenumbers import geocoder
from typing import Union
import phonenumbers
import requests
import re

from src.utils.logger import logger
from src.utils.functions import *

class Telegram:
    def __init__(
        self,
        session_folder: str = 'sessions',
        session_name: str = None,
        phone_number: str = None,
        api_hash: str = None,
        api_id: int = None, 
        app_version: str = None, 
        system_version: str = None, 
        device_model: str = None, 
        lang_code: str = 'en', 
        system_lang_code: str = 'en-us',
        lang_pack: str = '',
        proxy: dict = None
    ) -> None:
        self.phone_number = phone_number
        self.session_folder = session_folder
        self.session_name = session_name
        
        self.SUPPORTED_MODES = {
            "google": {
                "installer": "com.android.vending",
                "package_id": "org.telegram.messenger"
            },
            "standalone": {
                "installer": "com.android.packageinstaller",
                "package_id": "org.telegram.messenger.web"
            }
        }
        
        self.push_token = 'dct1tlUOQZuy0etJnolkEU:APA91bFIeDdCY88IhdtZIHFvre6ykucov4MYwvmVgMpn0YDdC4DlWUbziSCHIeZOasZ29mYvEDpMG0VUY7BZES_mrvKQnMujEhT_bOSvZMMLR9RgLtSqLfI'
        
        if lang_pack == 'tdesktop':
            params = types.JsonObject([
                types.JsonObjectValue('tz_offset', types.JsonNumber(
                    self.convert_timezone(timezone=self.get_timezone(phone_number=self.phone_number))
                ))
            ])
        elif lang_pack == 'android':
            params = types.JsonObject([
                types.JsonObjectValue('device_token', types.JsonString(self.push_token)),
                types.JsonObjectValue('data', types.JsonString("49C1522548EBACD46CE322B6FD47F6092BB745D0F88082145CAF35E14DCC38E1")),
                types.JsonObjectValue('installer', types.JsonString(self._installer('google'))),
                types.JsonObjectValue('package_id', types.JsonString(self._package_id('google'))),
                types.JsonObjectValue('tz_offset', types.JsonNumber(
                    self.convert_timezone(timezone=self.get_timezone(phone_number=self.phone_number))
                )),
                types.JsonObjectValue('perf_cat', types.JsonNumber(2)),
            ])
        
        self.client = TelegramClient(
            session=f'{self.session_folder}/{self.phone_number if session_name is None else self.session_name}',
            api_id=api_id,
            api_hash=api_hash,
            device_model=device_model,
            app_version=app_version,
            system_version=system_version,
            lang_code=lang_code,
            system_lang_code=system_lang_code,
            lang_pack=lang_pack,
            params=params,
            proxy=proxy
        )
    
    # -------------------------------------------- #
    
    def get_country_name(self, phone_number: str) -> Union[str, bool]:
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            return geocoder.description_for_number(parsed_number, 'en')
        except Exception as error:
            logger.error(f'[-][get_country_name] -> Error: {error}')
            return False

    def get_timezone(self, phone_number: str) -> Union[str, bool]:
        try:
            country_name = self.get_country_name(phone_number)
            if not country_name:
                return False

            response = requests.get(f'https://www.timeanddate.com/time/zone/{country_name}')
            match = re.search(r'UTC\s([+-]\d{1,2}(:\d{2})?)', response.text)
            return match.group(1) if match else False
        except Exception as error:
            logger.error(f'[-][get_timezone] -> Error: {error}')
            return False

    def convert_timezone(self, timezone: str) -> int:
        if timezone:
            sign = 1 if '+' in timezone else -1
            hours, _, minutes = timezone.lstrip('+-').partition(':')
            return sign * (int(hours) * 3600 + int(minutes or 0) * 60)
        return 0
    
    # -------------------------------------------- #
    
    def _package_id(self, mode):
        if mode not in self.SUPPORTED_MODES or 'package_id' not in self.SUPPORTED_MODES[mode]:
            raise RuntimeError(f"Invalid mode '{mode}'")
        return self.SUPPORTED_MODES[mode]['package_id']

    def _installer(self, mode: str):
        if mode not in self.SUPPORTED_MODES or 'installer' not in self.SUPPORTED_MODES[mode]:
            raise RuntimeError(f"Invalid mode '{mode}'")
        return self.SUPPORTED_MODES[mode]['installer']
    
    # -------------------------------------------- #
    
    async def get_me(self) -> dict:
        try:
            await self.client.connect()
            return await self.client.get_me()
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.get_me] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    async def is_banned(self) -> bool:
        try:
            await self.client.connect()
            if not await self.client.is_user_authorized():
                return 'invalid'
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.is_banned] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    # -------------------------------------------- #
    
    async def session_to_string(self) -> Union[str, bool]:
        try:
            string_session = StringSession.save(self.client.session)
            return string_session
        except Exception as error:
            logger.error(f'[-][Telegram.session_to_string] Error: {error}')
            return False
    
    async def string_to_session(string_session: str, session_name: str) -> bool:
        try:
            in_string = StringSession(string_session)
            out_sql = SQLiteSession(session_name)
            out_sql.auth_key = in_string.auth_key
            out_sql.set_dc(in_string.dc_id, in_string.server_address, in_string.port)
            out_sql.save()
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.string_to_session] Error: {error}')
            return 'unsuccess'
    
    # -------------------------------------------- #
    
    async def clear_all_data(self) -> bool:
        try:
            await self.client.connect()
            async for dialog in self.client.iter_dialogs():
                await dialog.delete()
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.clear_all_data] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    async def leave_all_channels(self) -> bool:
        try:
            await self.client.connect()
            async for dialog in self.client.iter_dialogs():
                if dialog.is_channel and not dialog.is_group:
                    await dialog.delete()
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.leave_all_channels] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    async def leave_all_groups(self) -> bool:
        try:
            await self.client.connect()
            async for dialog in self.client.iter_dialogs():
                if dialog.is_group and not dialog.is_channel:
                    await dialog.delete()
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.leave_all_groups] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()

    async def delete_all_chats(self) -> bool:
        try:
            await self.client.connect()
            async for dialog in self.client.iter_dialogs():
                await dialog.delete()
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.delete_all_chats] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()

    async def delete_all_contacts(self) -> bool:
        try:
            await self.client.connect()
            contacts = await self.client(functions.contacts.GetContactsRequest(hash=0))
            await self.client(functions.contacts.DeleteContactsRequest(contacts.users))
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.delete_all_contacts] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()

    async def join_chat(self, username) -> bool:
        try:
            await self.client.connect()
            await self.client(functions.channels.JoinChannelRequest(channel=username))
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.join_chat] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()

    async def left_chat(self, username) -> bool:
        try:
            await self.client.connect()
            await self.client(functions.channels.LeaveChannelRequest(channel=username))
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.left_chat] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    # -------------------------------------------- #
    
    async def update_profile(self, profile_photo: str = None, first_name: str = None, last_name: str = None, user_name: str = None, about: str = None) -> bool:
        try:
            await self.client.connect()
            if profile_photo:
                await self.client(functions.photos.UploadProfilePhotoRequest(file=await self.client.upload_file(profile_photo)))
            elif first_name:
                await self.client(functions.account.UpdateProfileRequest(first_name=first_name))
            elif last_name:
                await self.client(functions.account.UpdateProfileRequest(last_name=last_name))
            elif user_name:
                await self.client(functions.account.UpdateUsernameRequest(username=user_name))
            elif about:
                await self.client(functions.account.UpdateProfileRequest(about=about))
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.update_profile] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    
    async def delete_profile(self, last_name: bool = False, user_name: bool = False, about: bool = False, profile_photo: bool = False) -> bool:
        try:
            await self.client.connect()
            if last_name:
                res = await self.client(functions.account.UpdateProfileRequest(last_name=''))
                print(res)
            elif user_name:
                await self.client(functions.account.UpdateUsernameRequest(username=''))
            elif about:
                await self.client(functions.account.UpdateProfileRequest(about=''))
            elif profile_photo:
                await self.client(functions.photos.DeletePhotosRequest(await self.client.get_profile_photos('me')))
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.update_profile] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()      
    
    # -------------------------------------------- #
    
    async def enable_2fa(self, current_password: str, new_password: str, hint: str = '') -> bool:
        try:
            await self.client.connect()
            await self.client.edit_2fa(current_password=current_password, new_password=new_password, hint=hint)
            return 'success'
        except errors.rpcerrorlist.PasswordHashInvalidError:
            return 'unsuccess'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.enable_2fa] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    async def disable_2fa(self, current_password: str) -> bool:
        try:
            await self.client.connect()
            await self.client.edit_2fa(current_password=current_password, new_password = None)
            return 'success'
        except errors.rpcerrorlist.PasswordHashInvalidError:
            return 'unsuccess'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.enable_2fa] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
    async def reset_2fa(self) -> bool:
        try:
            await self.client.connect()
            await self.client(functions.account.ResetPasswordRequest())
            return 'success'
        except errors.rpcerrorlist.UserDeactivatedError:
            return 'invalid'
        except Exception as error:
            logger.error(f'[-][Telegram.reset_2fa] Error: {error}')
            return 'unsuccess'
        finally:
            await self.client.disconnect()
    
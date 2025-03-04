from telethon import Button

from src.database.models import redis_db
from src.config.config import SETTINGS

def support() -> list:
    return [
        [Button.url('Support', url=f'https://t.me/{SETTINGS.SUPPORT}')]
    ]

def start_key() -> list:
    return [
        [Button.text('• Account / Profile Functions', resize = True)],
        [Button.text('Check session'), Button.text('Check spam'), Button.text('Check T-data')],
        [Button.text('Session to json'), Button.text('Session to txt'), Button.text('Session to string')],
        [Button.text('T-data to session'), Button.text('Session to T-data')],
        [Button.text('Enable 2FA'), Button.text('Reset 2FA'), Button.text('Disable 2FA')],
        [Button.text('• Extract zip files (accounts)'), Button.text('• Mix zip files (accounts)')]
    ]

def account_functions_key() -> list:
    return [
        [Button.text('• Relogin tools (off)', resize = True)],
        [Button.text('• Functions'), Button.text('• Profile')],
        [Button.text('🔙 back')]
    ]

def functions_key() -> list:
    return [
        [Button.text('Clear All Data')],
        [Button.text('Leave All Channels'), Button.text('Leave All Groups')],
        [Button.text('Delete All Chats'), Button.text('Delete All Contacts')],
        [Button.text('Join Channel/Group'), Button.text('Leave Channel/Group')],
        [Button.text('Start bot (off)'), Button.text('Start web-app (off)')],
        [Button.text('Send message (off)')],
        [Button.text('🔙 back')]
    ]

def profile_key() ->list:
    return [
        [Button.text('Update Profile Photo (off)', resize = True)],
        [Button.text('Update Name'), Button.text('Update LastName')],
        [Button.text('Update UserName'), Button.text('Update Bio')],
        [Button.text('--------------------')],
        [Button.text('Delete Profile Photo')],
        [Button.text('Delete UserName'), Button.text('Delete LastName')],
        [Button.text('Delete Bio')],
        [Button.text('🔙 back')]
    ]

def finish_upload_key(finished: bool = False) -> list:
    if finished:
        return [
            [Button.inline('✅ Finished', data='finished')]
        ]
    return [
        [Button.inline('☑️ Finish upload', data='finish_upload')]
    ]

def update_settings_key() -> list:
    return [
        [Button.inline('🔄 Update status', data='update_settings')],
    ]

def change_settings_key() -> list:
    return [
        [Button.inline('🔄 Update status', data='update_settings')],
        [Button.inline('Change api-id', data='change-app_id'), Button.inline('Change api-hash', data='change-app_hash')],
        [Button.inline('Change device-model', data='change-device_model'), Button.inline('Change app-version', data='change-app_version')],
        [Button.inline('Change sdk-version', data='change-sdk_version'), Button.inline('Change platform', data='change-platform')],
        [Button.inline('Change first-name', data='change-first_name'), Button.inline('Change last-name', data='change-last_name')],
        [Button.inline('Change username', data='change-username'), Button.inline('Change twoFA password', data='change-twoFA')],
        [Button.inline('Change system-lang-code', data='change-system_lang_code'), Button.inline('Change lang-code', data='change-lang_code')],
        [Button.inline('Change lang-pack', data='change-lang_pack')],
        [Button.inline(f'🔢 Set batch size (Current-value: {redis_db.get("batch_size").decode("utf-8")})', data='change-batch_size')],
    ]

def back_to_json_settings_key() -> list:
    return [
        [Button.inline('🔙 back', data='back_to_json_settings')]
    ]

def back_key() -> list:
    return [
        [Button.text('🔙 back', resize = True)]
    ]

def admin_panel_key() -> list:
    return [
        [Button.text('📊 Bot stat', resize = True)],
        [Button.text('🟢 Open user'), Button.text('🔴 Close user')],
        [Button.text('🔙 back')]
    ]

def select_ready_date() -> list:
    return [
        [Button.text('Open for test (30 minutes)', resize = True)],
        [Button.text('1 day'), Button.text('2 day'), Button.text('3 day')],
        [Button.text('5 day'), Button.text('10 day'), Button.text('15 day')],
        [Button.text('1 month'), Button.text('2 month'), Button.text('3 month')],
        [Button.text('🔙 back to admin', resize = True)]
    ]

def back_to_admin_panel_key() -> list:
    return [
        [Button.text('🔙 back to admin', resize = True)]
    ]
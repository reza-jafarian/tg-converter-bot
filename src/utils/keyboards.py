from telethon import Button

def start_key() -> list:
    return [
        [Button.text('• Account / Profile Functions', resize = True)],
        [Button.text('Check session'), Button.text('Check T-data')],
        [Button.text('Session to json'), Button.text('Session to txt'), Button.text('Session to string')],
        [Button.text('T-data to session'), Button.text('Session to T-data')],
        [Button.text('Enable 2FA'), Button.text('Reset 2FA'), Button.text('Disable 2FA')]
    ]

def account_functions_key() -> list:
    return [
        [Button.text('• Functions', resize = True), Button.text('• Profile')],
        [Button.text('🔙 back')]
    ]

def functions_key() -> list:
    return [
        [Button.text('Clear All Data')],
        [Button.text('Leave All Channels'), Button.text('Leave All Groups')],
        [Button.text('Delete All Chats'), Button.text('Delete All Contacts')],
        [Button.text('Join Channel/Group'), Button.text('Leave Channel/Group')],
        [Button.text('🔙 back')]
    ]

def profile_key() ->list:
    return [
        [Button.text('Update Profile Photo (off)', resize = True)],
        [Button.text('Update Name'), Button.text('Update LastName')],
        [Button.text('Update UserName')],
        [Button.text('Delete Profile Photo (off)')],
        [Button.text('Delete UserName'), Button.text('Delete Bio')],
        [Button.text('🔙 back')]
    ]

def back_key() -> list:
    return [
        [Button.text('🔙 back', resize = True)]
    ]
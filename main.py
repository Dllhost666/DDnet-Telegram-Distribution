from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError, PasswordHashInvalidError
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.channels import JoinChannelRequest

def print_banner():
    banner = """
    ===================================
                DLLHOST
    ===================================
    Made by https://github.com/Dllhost666
    """
    print(banner)

def get_language():
    while True:
        language = input("Выберите язык / Choose language (RU/US): ").strip().upper()
        if language in ['RU', 'US']:
            return language
        else:
            print("Неверный выбор. Пожалуйста, введите RU или US.\nInvalid choice. Please enter RU or US.")

def get_client(api_id, api_hash, language):
    if language == 'RU':
        phone_prompt = "Введите номер телефона (с кодом страны): "
        code_prompt = 'Введите код из Telegram: '
        password_prompt = 'Введите пароль (двухфакторная аутентификация): '
        password_error = "Неверный пароль. Попробуйте снова."
    else:
        phone_prompt = "Enter phone number (with country code): "
        code_prompt = 'Enter the code from Telegram: '
        password_prompt = 'Enter password (two-factor authentication): '
        password_error = "Invalid password. Please try again."

    phone = input(phone_prompt)
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        try:
            client.send_code_request(phone)
            code = input(code_prompt)
            client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input(password_prompt)
            try:
                client.sign_in(password=password)
            except PasswordHashInvalidError:
                print(password_error)
                client.disconnect()
                return None

    return client

def get_channels(language):
    if language == 'RU':
        channels_prompt = "Введите ссылки на Telegram каналы (разделенные пробелом, не более 15): "
        channels_error = "Превышено максимальное количество каналов (15). Попробуйте снова."
        link_error = "Неверная ссылка на канал: {}. Все ссылки должны начинаться с 'https://t.me/'"
    else:
        channels_prompt = "Enter links to Telegram channels (separated by space, no more than 15): "
        channels_error = "Exceeded maximum number of channels (15). Please try again."
        link_error = "Invalid channel link: {}. All links must start with 'https://t.me/'"

    channels = input(channels_prompt).split()
    if len(channels) > 15:
        print(channels_error)
        return None
    for channel in channels:
        if not channel.startswith("https://t.me/"):
            print(link_error.format(channel))
            return None
    return channels

def get_message(language):
    if language == 'RU':
        message_prompt = "Введите сообщение для рассылки (используйте \\n для переноса строки): "
    else:
        message_prompt = "Enter the message to be sent (use \\n for line breaks): "

    message = input(message_prompt)
    return message.replace("\\n", "\n")

def send_message(client, channels, message, language):
    if language == 'RU':
        success_message = "Сообщение отправлено в {}"
        error_message = "Ошибка при отправке сообщения в {}: {}"
    else:
        success_message = "Message sent to {}"
        error_message = "Error sending message to {}: {}"

    for channel in channels:
        try:
            client(JoinChannelRequest(channel.split('/')[-1]))
            client(SendMessageRequest(channel.split('/')[-1], message))
            print(success_message.format(channel))
        except Exception as e:
            print(error_message.format(channel, e))

def main():
    print_banner()
    language = get_language()
    if language == 'RU':
        api_id_prompt = "Введите API ID: "
        api_hash_prompt = "Введите API HASH: "
    else:
        api_id_prompt = "Enter API ID: "
        api_hash_prompt = "Enter API HASH: "

    api_id = input(api_id_prompt)
    api_hash = input(api_hash_prompt)

    while True:
        client = None
        while not client:
            client = get_client(api_id, api_hash, language)

        channels = None
        while not channels:
            channels = get_channels(language)

        message = get_message(language)
        send_message(client, channels, message, language)
        if language == 'RU':
            print("Рассылка завершена. Перезапуск программы...\n")
        else:
            print("Mailing completed. Restarting the program...\n")
        client.disconnect()

if __name__ == "__main__":
    main()

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

def get_client(api_id, api_hash):
    phone = input("Введите номер телефона (с кодом страны): ")
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        try:
            client.send_code_request(phone)
            code = input('Введите код из Telegram: ')
            client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input('Введите пароль (двухфакторная аутентификация): ')
            try:
                client.sign_in(password=password)
            except PasswordHashInvalidError:
                print("Неверный пароль. Попробуйте снова.")
                client.disconnect()
                return None

    return client

def get_channels():
    channels = input("Введите ссылки на Telegram каналы (разделенные пробелом, не более 15): ").split()
    if len(channels) > 15:
        print("Превышено максимальное количество каналов (15). Попробуйте снова.")
        return None
    for channel in channels:
        if not channel.startswith("https://t.me/"):
            print(f"Неверная ссылка на канал: {channel}. Все ссылки должны начинаться с 'https://t.me/'")
            return None
    return channels

def get_message():
    message = input("Введите сообщение для рассылки (используйте \\n для переноса строки): ")
    return message.replace("\\n", "\n")

def send_message(client, channels, message):
    for channel in channels:
        try:
            client(JoinChannelRequest(channel.split('/')[-1]))
            client(SendMessageRequest(channel.split('/')[-1], message))
            print(f"Сообщение отправлено в {channel}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения в {channel}: {e}")

def main():
    print_banner()
    api_id = input("Введите API ID: ")
    api_hash = input("Введите API HASH: ")

    while True:
        client = None
        while not client:
            client = get_client(api_id, api_hash)

        channels = None
        while not channels:
            channels = get_channels()

        message = get_message()
        send_message(client, channels, message)
        print("Рассылка завершена. Перезапуск программы...\n")
        client.disconnect()

if __name__ == "__main__":
    main()

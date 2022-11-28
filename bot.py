import os
import asyncio
import objects
from objects import time_now, GoogleDrive
from telethon.sync import TelegramClient, events
# =================================================================================================================
stamp1 = time_now()
Auth = objects.AuthCentre(ID_DEV=os.environ['ID_DEV'], TOKEN=os.environ['TOKEN'])


def sessions_creation():
    objects.environmental_files()
    drive_client = GoogleDrive('google.json')
    for file in drive_client.files():
        user_session = f"{os.environ['session']}.session"
        if file['name'] == user_session:
            drive_client.download_file(file['id'], f'{user_session}')
            Auth.dev.printer(f'Скачали сессию Telegram: {user_session}')
# =================================================================================================================


def start(stamp):
    try:
        sessions_creation()
        if os.environ.get('local'):
            Auth.dev.printer(f'Запуск скрипта локально за {time_now() - stamp} сек.')
        else:
            Auth.dev.start(stamp1)
            Auth.dev.printer(f'Скрипт запущен за {time_now() - stamp} сек.')
        asyncio.set_event_loop(asyncio.new_event_loop())
        client = TelegramClient(os.environ['session'], int(os.environ['api_id']), os.environ['api_hash']).start()
        with client:
            Auth.dev.printer(f"Сессия в работе: {os.environ['session']}")

            @client.on(events.NewMessage(chats=os.environ['chat']))
            async def response_user_update(response):
                await client.forward_messages(int(os.environ['target_chat_id']), response.message)

            client.run_until_disconnected()
    except IndexError and Exception:
        Auth.dev.thread_except()


if os.environ.get('local'):
    start(stamp1)

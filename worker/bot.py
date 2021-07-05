import os
import asyncio
import objects
import _thread
from time import sleep
from objects import time_now, GoogleDrive
from telethon.sync import TelegramClient, events
from datetime import datetime, timezone, timedelta
# =================================================================================================================
stamp1 = time_now()
Auth = objects.AuthCentre(ID_DEV=-1001312302092, TOKEN=os.environ['TOKEN'])


def sessions_creation():
    objects.environmental_files()
    drive_client = GoogleDrive('google.json')
    for file in drive_client.files():
        user_session = f"{os.environ['session']}.session"
        if file['name'] == user_session:
            drive_client.download_file(file['id'], f'{user_session}')
            Auth.dev.printer(f'Скачали сессию Telegram: {user_session}')


sessions_creation()
tz = timezone(timedelta(hours=3))
# =================================================================================================================


def auto_reboot():
    reboot = None
    while True:
        try:
            sleep(30)
            date = datetime.now(tz)
            if date.strftime('%H') == '01' and date.strftime('%M') == '59':
                reboot = True
                while date.strftime('%M') == '59':
                    sleep(1)
                    date = datetime.now(tz)
            if reboot:
                reboot = None
                text, _ = Auth.logs.reboot()
                Auth.dev.printer(text)
        except IndexError and Exception:
            Auth.dev.thread_except()


def start(stamp):
    try:
        if os.environ.get('local'):
            Auth.dev.printer(f'Запуск скрипта локально за {time_now() - stamp} сек.')
        else:
            Auth.dev.start(stamp1)
            _thread.start_new_thread(auto_reboot, ())
            Auth.dev.printer(f'Скрипт запущен за {time_now() - stamp} сек.')
        asyncio.set_event_loop(asyncio.new_event_loop())
        client = TelegramClient(os.environ['session'], int(os.environ['api_id']), os.environ['api_hash']).start()
        with client:
            Auth.dev.printer(f"Сессия в работе: {os.environ['session']}")

            @client.on(events.NewMessage(chats=os.environ['chat']))
            async def response_user_update(response):
                await client.forward_messages(-1001532518410, response.message)

            client.run_until_disconnected()
    except IndexError and Exception:
        Auth.dev.thread_except()


if os.environ.get('local'):
    start(stamp1)

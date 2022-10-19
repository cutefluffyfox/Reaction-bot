import datetime
import re

from os import getenv
from asyncio import sleep
from random import random
from collections import defaultdict

from pyrogram import Client, filters
from pyrogram.types import MessageEntity
from pyrogram.enums import MessageEntityType, ParseMode
from pyrogram.types.messages_and_media.message import Message

import dotenv


dotenv.load_dotenv(dotenv.find_dotenv())
api_id = getenv('API_ID')
api_hash = getenv('API_HASH')

app = Client("my_account", api_id=api_id, api_hash=api_hash)

DR_INFO = {}

EMOJI_INFO = {
    'blank': {
        'text': '🚶‍♂',
        'id': 5463010113440717314,
    },
    'man': {
        'text': '👀',
        'id': 5235693192568905268
    }
}


@app.on_message(filters.text & filters.me)
async def echo(client, message: Message):
    if message.text == '$walk':
        for _ in range(4):
            for i in range(8):
                text = ""
                for j in range(8):
                    emoji = (EMOJI_INFO['man'] if i == j else EMOJI_INFO['blank'])['text']
                    emoji_id = (EMOJI_INFO['man'] if i == j else EMOJI_INFO['blank'])['id']
                    text += f'<emoji id="{emoji_id}">{emoji}</emoji>'

                await app.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.id,
                    text=text,
                    parse_mode=ParseMode.HTML
                )
                await sleep(0.4)
        await app.delete_messages(chat_id=message.chat.id, message_ids=message.id)
    if message.text == '$понос':
        await app.edit_message_text(message.chat.id, message.id, 'Если выпадет 1, то у тебя понос')
        await app.send_dice(chat_id=message.chat.id)
    # if message.text.startswith("$set_dr "):
    #     dr = message.text[len('$set_dr'):]
    #     day = datetime.datetime.now()

        # DR_INFO[day].append(dr)


@app.on_message(filters.text)
async def not_me(client, message: Message):
    now = datetime.datetime.now()
    if (now.month == 10 and now.day == 20) and message.text in ['/polina_s_dr', '/polya_s_dr', '/pinka_s_dr']:
        await sleep(random() * 10)
        await message.react(emoji="❤️‍🔥")
    if {'лиса', 'лисичка', 'фырка', 'лисик', 'лис', 'фырочка',
        'лисы', 'лисички', 'фырки', 'лисики', 'fox', 'foxes',
        'лися', 'лисица', 'лисицы'} & set(re.sub(r"\W+", ' ', message.text.lower()).split()):
        await message.react(emoji='😍')
    if '@cutefluffyfox' in message.text.lower().split():
        # await message.reply(text='Привет, я Полинина ассистентка. Я сохранила ваше сообщение, в ближайшее время она вам на него ответит🌟')
        await message.forward(chat_id=app.me.id, disable_notification=False)
        await app.send_message(chat_id=app.me.id, text=message.link)


app.run()

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiohttp import ClientSession

import time
import wikipedia
from config import API_TOKEN
from googletrans import Translator

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

wikipedia.set_lang('uz')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Assalomu aleykum, {message.from_user.full_name}!\n\nQidirayotgan maqolangiz uchun kalit so'zlarni kiriting yuboring yoki @wikipedio_bot so'zidan so'ng kalit so'zni yozing")    



@dp.message_handler()
# async def tarjima(message: types.Message):
#     translator =  Translator()
#     lang = translator.detect(message.text).lang
#     dest = 'uz' if lang == 'en' else 'uz'

#     word_id = translator.translate(message.text, dest=dest).text

async def sendWiki(message: types.Message):
    try:
        respond = wikipedia.page(message.text)
        respond2 = wikipedia.summary(message.text)
        # pprint(respond.content)
        await bot.send_photo(chat_id=message.from_user.id, photo=respond.images[0])
        await message.answer(f"{respond.title.upper()} \n\n {respond2}")

    except wikipedia.exceptions.DisambiguationError as e:
        logging.info(e) 

    except Exception as e:
        logging.info(e)
        await message.answer(f" Hurmatli {message.from_user.full_name} afsuski, bu mavzuga oid o'zbek tilida maqola topilmadi.\nUshbu mavzuga oid maqola yozib O'zbek tilidagi Wikipedia rivojiga o'z hissangizni qo'sha olasiz. Shu bilan birga WikiMarafonda qatnashib pul yutug'lariga ham ega bo'lishingiz mumkin. WikiStipendiya haqida ba'tafsil ma'lumot olish uchun quyidagi manzilni ziyorat qiling: https://t.me/wikistipendiya \n\n \"Wikipedia siz kabi insonlar tomonidan yaratildi\"")
        # await message.answer(f"Hurmatli {message.from_user.full_name} afsuski, bu mavzu bo'yicha maqola topilmadi")

async def empty_query(query: types.InlineQuery):
    lang = translator.detect(message.text).lang
    
    if lang == 'en':
        word_id = translator.translate(message.text, dest='uz').text

    time.sleep(1)
    if not query.query == " ":
        try:
            que = wikipedia.search(query.query.lower(), results=3)
            resultSearch = []
            for qu in que:
                resultSearch.append(
                    types.InlineQueryResultArticle(
                        id=qu,
                        title=qu,
                        input_message_content=types.InputTextMessageContent(
                            message_text=qu
                        ),
                
                    )
                )
            await query.answer(
                resultSearch
            )
            # await State.inlineQuery.set()
        except wikipedia.exceptions.DisambiguationError as e:
            pprint(e.options)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

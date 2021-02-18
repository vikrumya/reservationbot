import logging
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
import requests
import re
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
API_TOKEN = '1143625866:AAG7kyt1d2FZQoSlXWAXfje1TAkGg0TriCM'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
button_fairford = KeyboardButton('Fairford')
fairford_kb = ReplyKeyboardMarkup()
fairford_kb.add(button_fairford)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm ReservationBot!\nPowered by Victor.")

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    url = 'https://www.notams.faa.gov/dinsQueryWeb/queryRetrievalMapAction.do?retrieveLocId=EGVA&actionType=notamRetrievalByICAOs'
    page = requests.get(url).content.decode('utf-8')
    new_news = []
    soup = BeautifulSoup(page, "html.parser")
    news = soup.findAll('td', class_='textBlack12')
    print(news)
    for new in news:
        new_news.append(new.get_text())
    new_news = str(new_news)
    new_news = re.sub("\n", "", new_news)
    print(new_news)
    await message.reply(new_news, reply_markup=fairford_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     if message.text == 'новости':
#         bot.send_message(message.chat.id, new_news[i])
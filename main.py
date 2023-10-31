import telebot
from telebot.types import InputMediaPhoto
# from dotenv import load_dotenv
import os
from os.path import join, dirname
import re
from parse_photo import parse_photo

def get_from_env(key):
  # dotenv_path = join(dirname(__file__), 'token.env')
  # load_dotenv(dotenv_path)
  return os.environ.get(key)

token = get_from_env('BOT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """Привет! Отправь ссылку на объявление с ЦИАНа, и я пришлю тебе фотографии из него""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(message))
    if(url):
        bot.reply_to(message,"Секундочку...")
    link = url[0].split('\'')[0]
    title1, title2, desc, photos = parse_photo(link)
    bot.reply_to(message, f'*Объявление*: {title2}\n\n*Подзаголовок*: {title1}\n\n*Описание*: {desc}',parse_mode= 'Markdown')
    for count, element in enumerate(photos, 0):
        if count % 10 == 0:
            all_photos = []
            if (len(photos) >= count + 10):
                right_val = count + 10
            else:
                right_val = len(photos)
            for i in range (count, right_val):
                mediaPhoto = InputMediaPhoto(photos[i],f'{title2}\n{title1}')
                all_photos.append(mediaPhoto)
            bot.send_media_group(message.chat.id, all_photos)

bot.polling(none_stop = True)

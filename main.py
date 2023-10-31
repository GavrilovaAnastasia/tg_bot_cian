import telebot
from telebot.types import InputMediaPhoto
# from dotenv import load_dotenv
import os
# from os.path import join, dirname
import re
from parse_photo import parse_photo
from functools import wraps


def get_from_env(key):
  # dotenv_path = join(dirname(__file__), 'token.env')
  # load_dotenv(dotenv_path)
  return os.environ.get(key)

token = get_from_env('BOT_TOKEN')
bot = telebot.TeleBot(token)


def private_access():
    def deco_restrict(f):
        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            user_id = message.from_user.id
            perm_list = get_from_env('PERMISSION_LIST').split(",")
            if str(user_id) in perm_list:
                return f(message, *args, **kwargs)
            else:
                bot.reply_to(message, text='Кто ты? Иди отсюда')
        return f_restrict
    return deco_restrict


@bot.message_handler(commands=['start'])
@private_access()
def send_welcome(message):
    bot.reply_to(message, """Привет! Отправь ссылку на объявление с ЦИАНа, и я пришлю тебе фотографии из него""")


@bot.message_handler(func=lambda message: True)
@private_access()
def send_photos(message):
    urls = re.findall(r'(https?://[^\s]+)', str(message.text))
    if urls:
        bot.reply_to(message, "Секундочку...")
        sent_flats = []
        for ur in list(set(urls)):
            link = ur.split('\'')[0].replace("\\n", "")
            res = parse_photo(link)
            if len(res) == 1:
                if res[0] == -1:
                    bot.reply_to(message, f'Ссылка {link} недействительна')
                elif res[1] == -2:
                    bot.reply_to(message, f'Не удалось получить данные по ссылке {link}')
            else:
                if res[0] not in sent_flats:
                    sent_flats.append(res[0])
                    bot.reply_to(message, f'*Объявление*: {res[2]}\n\n*Подзаголовок*: {res[1]}\n\n*Описание*: {res[3]}', parse_mode= 'Markdown')
                    for count, element in enumerate(res[4], 0):
                        if count % 10 == 0:
                            all_photos = []
                            if len(res[4]) >= count + 10:
                                right_val = count + 10
                            else:
                                right_val = len(res[4])
                            for i in range (count, right_val):
                                mediaphoto = InputMediaPhoto(res[4][i], f'{res[2]}\n{res[1]}')
                                all_photos.append(mediaphoto)
                            bot.send_media_group(message.chat.id, all_photos)
    else:
        bot.reply_to(message, "Ссылка не распознана :(")


bot.polling(none_stop=True)

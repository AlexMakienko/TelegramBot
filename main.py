import telebot
import traceback
from config import TOKEN, keys
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать! \n помощь :/help \n Список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n \
- имя валюты цену которой Вы хотите узнать \n - имя валюты в которой надо узнать цену первой валюты \
\n - количество первой валюты \n вводим через пробел \n Список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Необходимо ввести три параметра! (/help)')
        total = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        base, quote, amount = values
        total = Converter.get_price(base, quote, amount)
        text = f'Цена {amount} {base} в {quote} - {total}'
        bot.send_message(message.chat.id, text)

bot.polling()





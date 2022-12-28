import telebot
import traceback
from extensions import APIException, Convertor
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def echo_test(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Приветствую, моё имя - Зубрик.'
                                      '\n Я - ваш помощник по переводу из одной валюты в другую.'
                                      '\n Что бы узнать как мной пользовать нажмите /help'
                                      '\n Что бы узнать какие валюты возможно использовать, нажмите /values.')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'На данный момент доступны эти валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    text = ('Всем чем я могу помочь, было обозначено ранее'
            '\n Я - ваш помощник по переводу из одной валюты в другую.'
            '\n Чтобы начать работу введите название валюты которую вы хотите перевести, '
            '\n а так же ту валюту в которую вы хотите перевести и номинал, например 100.'
            )
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)

from subprocess import call
import telebot
from telebot import types

bot = telebot.TeleBot('bot_key')

# @bot.message_handler()
# def get_user_test(message):
#     if message.text == 'Hello':
#         bot.send_message(message.chat.id, 'Hello')
#     elif message.text == "id":
#         bot.send_message(message.chat.id, message.from_user.id)
#     else: 
#         bot.send_message(message.chat.id, 'I don\'t understand you')


@bot.message_handler(commands=['search'])
def website(message):
    text = ' '.join(message.text.split()[1:])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Google', f'https://www.google.com/search?q={text}'))
    markup.add(types.InlineKeyboardButton('Yandex', f'https://yandex.ru/search/?lr=10743&text={text}'))

    bot.send_message(message.chat.id, 'Выберите поисковой сайт', reply_markup=markup)

bot.polling(none_stop=True)
import os
import telebot
token = "6102946467:AAGfioeQanwYS-TSyxvQNtoeqdnt_xCL92I"
bot = telebot.TeleBot(token)

try:
    os.system("python bot.py")
except:
    @bot.message_handler(content_types=["text"])
    def sand_message(message):
        bot.send_message(message.chat.id, "Произошла какая-то непредвиденная ошибка")

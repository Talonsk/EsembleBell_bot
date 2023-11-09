import telebot
import db
import os
from telebot import types

# Настояший токен: 6102946467:AAGfioeQanwYS-TSyxvQNtoeqdnt_xCL92I
# Тестовый токен: 6580465120:AAEZNj0PJEUy88QrxVEt-WS32lTkhu0yENQ

bot = telebot.TeleBot("6102946467:AAGfioeQanwYS-TSyxvQNtoeqdnt_xCL92I")
name = update_name = song_id = None
# bot.remove_webhook()

try:
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = (types.KeyboardButton("Найти текст песни"))
        button2 = (types.KeyboardButton("Загрузить текст песни"))
        button3 = (types.KeyboardButton("Удалить текст песни"))
        button4 = (types.KeyboardButton("Обновить текст песни"))
        button5 = (types.KeyboardButton("Список всех песен"))
        markup.row(button1, button2)
        markup.row(button3, button4)
        markup.add(button5)

        bot.send_message(message.chat.id, "Добро пожаловать", reply_markup=markup)


    @bot.message_handler(content_types=["text"])
    def check_answer(message):
        if message.text == "Найти текст песни":
            bot.send_message(message.chat.id, "Как назвывается ваша песня?")
            bot.register_next_step_handler(message, wait_answer)
        elif message.text == "Загрузить текст песни":
            bot.send_message(message.chat.id, "Отправте название песни в чат:")
            bot.register_next_step_handler(message, wait_name)
        elif message.text == "Удалить текст песни":
            bot.send_message(message.chat.id, "Отправте название песни, которую хотите удалить из базы данных, в чат:")
            bot.register_next_step_handler(message, wait_delit_name)
        elif message.text == "Обновить текст песни":
            bot.send_message(message.chat.id, "Нужно обновить текст этой песни:")
            bot.register_next_step_handler(message, wait_update_name)
        elif message.text == "Список всех песен":
            list_of_song_name = db.list_of_all_songs()
            bot.send_message(message.chat.id, f"Вот список всех песен:\n{list_of_song_name}")




    def wait_answer(message):
        global song_id
        # try:
        name_of_song = message.text
        result = db.text_search(name_of_song)  # results = db.text_search
        song_id = result[0]
        song_text = result[1]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Фото текста", callback_data="photo"))
        bot.send_message(message.chat.id, f"Вот текст вашей песни:\n{song_text}", parse_mode="html", reply_markup=markup)
        # except (TypeError, IndexError):
        #     markup = types.InlineKeyboardMarkup()
        #     markup.add(types.InlineKeyboardButton("Попробовать ещё раз", callback_data="try_again"))
        #     bot.send_message(message.chat.id, "Такой песни нет в базе данных", reply_markup=markup)


    @bot.callback_query_handler(func=lambda callback: True)
    def call(callback):
        if callback.data == "try_again":
            bot.send_message(callback.message.chat.id, "Попробуйте использовать другой падеж или название/строчку песни")
            bot.register_next_step_handler(callback.message, wait_answer)
        elif callback.data == "photo":
            try:
                photo = db.upload_photo_song(song_id)
                #get_image = open(photo_path, "rb")
                bot.send_photo(callback.message.chat.id, photo)
                bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                              reply_markup=None)
            except TypeError:
                bot.send_message(callback.message.chat.id, "Фота этого текста ещё нет в бд")
        elif callback.data == "add_photo":
            bot.send_message(callback.message.chat.id, "Отправте фото текста в чат")
            bot.register_next_step_handler(callback.message.chat.id, wait_photo)

    def wait_name(message):
        global name
        name = message.text
        bot.send_message(message.chat.id, "Отправте текст песни в чат:")
        bot.register_next_step_handler(message, wait_text)

    def wait_text(message):
        try:
            text = message.text
            db.download_song_text(name, text)
            bot.send_message(message.chat.id, "Песня добавленна в список!")
        except:
            bot.send_message(message.chat.id, "Эта песня уже есть в базе данных")

    def wait_delit_name(message):
        try:
            delit_name = message.text
            result = db.text_search(delit_name)  # results = db.text_search
            delit_id = result[0]
            db.delite_song_text(delit_id)
            bot.send_message(message.chat.id, "Песня успешна удалена")
        except (TypeError, IndexError):
            bot.send_message(message.chat.id, "Этой песни ещё/уже нет в базе данных")

    def wait_update_name(message):
        global song_id
        try:
            update_name = message.text
            result = db.text_search(update_name)  # results = db.text_search
            song_id = result[0]
            bot.send_message(message.chat.id, "Отправте текст песни в чат:")
            bot.register_next_step_handler(message, wait_update_text)
        except (TypeError, IndexError):
            bot.send_message(message.chat.id, "Такой песни нет в базе данных")

    def wait_update_text(message):
        update_text = message.text
        db.update_song_text(update_text, song_id)
        bot.send_message(message.chat.id, "Текст песни успешно обнавлен")

    def wait_photo(message):
        image = message.text

    bot.polling(none_stop=True)
except BaseException as error:
    print(type(error), error)
    os.system("python bot.py")
# finally:
#     @bot.message_handler(content_types=["text"])
#     def check_answer(message):
#         if message.text == "":
#             bot.send_message(message.chat.id, "Произошла какая-то непредвиденная ошибка")




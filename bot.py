import telebot
import db
import os
from telebot import types


bot = telebot.TeleBot("6102946467:AAGfioeQanwYS-TSyxvQNtoeqdnt_xCL92I")
name = update_name = name_of_song = None
 # bot.remove_webhook()




try:
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Найти текст песни"))
        markup.add(types.KeyboardButton("Загрузить текст песни"))
        markup.add(types.KeyboardButton("Удалить текст песни"))
        markup.add(types.KeyboardButton("Обновить текст песни"))

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


    def wait_answer(message):
        global name_of_song
        try:
            name_of_song = message.text
            song_text = db.text_search(name_of_song)  # results = db.text_search
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Фото текста", callback_data="photo"))
            bot.send_message(message.chat.id, f"Вот текст вашей песни:\n{song_text}", parse_mode="html", reply_markup=markup)
        except (TypeError, IndexError):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Попробовать ещё раз", callback_data="try_again"))
            bot.send_message(message.chat.id, "Такой песни нет в базе данных", reply_markup=markup)


    @bot.callback_query_handler(func=lambda callback: True)
    def call(callback):
        if callback.data == "try_again":
            bot.send_message(callback.message.chat.id, "Попробуйте использовать другой падеж или название/строчку песни")
            bot.register_next_step_handler(callback.message, wait_answer)
        elif callback.data == "photo":
            photo = db.upload_photo_song(name_of_song)
            #get_image = open(photo_path, "rb")
            bot.send_photo(callback.message.chat.id, photo)
            bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                          reply_markup=None)
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
            db.delite_song_text(delit_name)
            bot.send_message(message.chat.id, "Песня успешна удалена")
        except TypeError:
            bot.send_message(message.chat.id, "Этой песни ещё/уже нет в базе данных")

    def wait_update_name(message):
        global update_name
        try:
            update_name = message.text
            bot.send_message(message.chat.id, "Отправте текст песни в чат:")
            bot.register_next_step_handler(message, wait_update_text)
        except TypeError:
            bot.send_message(message.chat.id, "Такой песни нет в базе данных")

    def wait_update_text(message):
        update_text = message.text
        db.update_song_text(update_text, update_name)
        bot.send_message(message.chat.id, "Текст песни успешно обнавлен")

    def wait_photo(message):
        image = message.text
        db.execute()
    bot.polling(none_stop=True)
except BaseException as error:
    print(error)

# finally:
#     @bot.message_handler(content_types=["text"])
#     def check_answer(message):
#         if message.text == "":
#             bot.send_message(message.chat.id, "Произошла какая-то непредвиденная ошибка")
    os.system("python bot.py")



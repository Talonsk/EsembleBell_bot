import telebot
import db
import file
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
        button1 = (types.KeyboardButton("Список всех песен"))
        button2 = (types.KeyboardButton("Найти текст песни"))
        button3 = (types.KeyboardButton("Загрузить текст песни"))
        button4 = (types.KeyboardButton("Удалить текст песни"))
        button5 = (types.KeyboardButton("Обновить текст песни"))
        button6 = (types.KeyboardButton("Загрузить фото песни"))

        markup.add(button1)
        markup.row(button2, button3)
        markup.row(button4, button5)
        markup.add(button6)

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
        elif message.text == "Загрузить фото песни":
            bot.send_message(message.chat.id, "Нужно загрузить фото этой песни:")
            bot.register_next_step_handler(message, wait_photo_name)
        elif message.text == "Список всех песен":
            list_of_song_name = db.list_of_all_songs()
            bot.send_message(message.chat.id, f"Вот список всех песен:\n{list_of_song_name}")




    def wait_answer(message):
        global song_id
        try:
            name_of_song = message.text
            result = db.text_search(name_of_song)
            song_id = result[0]
            song_text = result[1]
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
            try:
                photo = db.upload_photo_song(song_id)
                if photo != None:
                    bot.send_photo(callback.message.chat.id, photo)
                else:
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton("Загрузить фото", callback_data="add_photo"))
                    bot.send_message(callback.message.chat.id, "Фота этого текста ещё нет в бд", reply_markup=markup)

                bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                              reply_markup=None)

            except TypeError:
                bot.send_message(callback.message.chat.id, "По неизвестной причине нам не удается найти или отослать это фото")

        elif callback.data == "add_photo":
            bot.send_message(callback.message.chat.id, "Отправте фото текста в чат")
            bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                          reply_markup=None)
            bot.register_next_step_handler(callback.message, wait_photo)
        elif callback.data == "photo_again":
            bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                          reply_markup=None)
            bot.send_message(callback.message.chat.id, "Отправте фото песни в чат:")
            bot.register_next_step_handler(callback.message, wait_photo)

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
            result = db.text_search(delit_name)
            delit_id = result[0]
            db.delite_song_text(delit_id)
            bot.send_message(message.chat.id, "Песня успешна удалена")
        except (TypeError, IndexError):
            bot.send_message(message.chat.id, "Этой песни ещё/уже нет в базе данных")

    def wait_update_name(message):
        global song_id
        try:
            update_name = message.text
            result = db.text_search(update_name)
            song_id = result[0]
            bot.send_message(message.chat.id, "Отправте текст песни в чат:")
            bot.register_next_step_handler(message, wait_update_text)
        except (TypeError, IndexError):
            bot.send_message(message.chat.id, "Такой песни нет в базе данных")

    def wait_update_text(message):
        update_text = message.text
        db.update_song_text(update_text, song_id)
        bot.send_message(message.chat.id, "Текст песни успешно обнавлен")


    # @bot.message_handler(content_types=['photo'])
    def wait_photo_name(message):
        global song_id
        try:
            photo_name = message.text
            result = db.text_search(photo_name)
            song_id = result[0]
            bot.send_message(message.chat.id, "Отправте фото песни в чат:")
            bot.register_next_step_handler(message, wait_photo)
        except (TypeError, IndexError):
            bot.send_message(message.chat.id, "Такой песни нет в базе данных")

    def wait_photo(message):
        photo = message.photo
        if photo != None:
            if message.media_group_id == None:
                photo_id = photo[-1].file_id
                file_info = bot.get_file(photo_id)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(f'image.jpg', 'wb') as new_file:
                    new_file.write(downloaded_file)
                file.import_one_photo(song_id)
                os.remove(f'image.jpg')
                bot.send_message(message.chat.id, "Фото песни успешно загружено")
            else:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Поворить отправку", callback_data="photo_again"))
                bot.send_message(message.chat.id, "Нужно загрузить одно фото, а не несколько", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Это не фото!")


    bot.polling(none_stop=True)
except BaseException as error:
    print(type(error), error)
    os.system("python bot.py")
# finally:
#     pass
#     @bot.message_handler(content_types=["text"])
#     def check_answer(message):
#         bot.send_message(message.chat.id, "Произошла какая-то непредвиденная ошибка")





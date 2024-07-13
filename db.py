import sqlite3
import string
def execute(request, __parameters):
    conn = sqlite3.connect("SongBD.db")
    cursor = conn.cursor()
    result = cursor.execute(request, __parameters)
    result_performance = result.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result_performance

def text_search(search):
    conn = sqlite3.connect('SongBD.db')
    cursor = conn.cursor()
    low_search = search.lower()
    search_wo_punctuation = low_search.translate(str.maketrans("", "", string.punctuation))
    new_search = '%'+search_wo_punctuation+'%'
    cursor.execute("SELECT id, text FROM song WHERE low_name LIKE ? OR low_text LIKE ?", [new_search, new_search])
    text = cursor.fetchall()
    # print(cursor.fetchall())
    found_text = text[0]
    cursor.close()
    conn.close()
    return found_text

def upload_photo_song(song_id):
    conn = sqlite3.connect('SongBD.db')
    cursor = conn.cursor()
    cursor.execute("SELECT photo FROM song WHERE id = ?", [song_id])
    record = cursor.fetchone()
    photo = record[0]
    cursor.close()
    conn.close()
    return photo

def list_of_all_songs(list_of_song_name=""):
    conn = sqlite3.connect('SongBD.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM song")
    result = cursor.fetchall()
    for name_of_song in result:
        list_of_song_name += name_of_song[0]
    cursor.close()
    conn.close()
    return list_of_song_name

def download_song_text(name, text):
    name += "\n"
    low_name = name.lower() + "\n"
    low_text = text.lower()
    new_text = low_text.translate(str.maketrans("", "", string.punctuation))
    execute("INSERT INTO song (name, text, low_name, low_text) VALUES (?, ?, ?, ?)", (name, text, low_name, new_text))

def delite_song_text(delit_id):
    execute('DELETE FROM song WHERE id = ?', [delit_id])

def update_song_text(update_text, song_id):
    low_update_text = update_text.lower()
    new_update_text = low_update_text.translate(str.maketrans("", "", string.punctuation))
    execute("UPDATE song SET text = ?, low_text = ? WHERE id = ?", (update_text, new_update_text, song_id))


#Загрузка текстов и изображений через файлы
def import_text_of_song():
    result = []
    for x in range(1, 52):
        text = open(f"./text/text{x}.txt", "r", encoding="utf-8")
        for line in text:
            result.append(line)
        name_of_song = result[0]
        result.remove(name_of_song)
        text_of_song = ''.join(result)
        execute("INSERT INTO song (name, text) VALUES (?, ?)", (name_of_song, text_of_song))
        result.clear()

def import_low_text_of_song():
    result = []
    for x in range(1, 52):
        text = open(f"./text/text{x}.txt", "r", encoding="utf-8")
        for line in text:
            low_line = line.lower()
            new_line = low_line.translate(str.maketrans("", "", string.punctuation))
            result.append(new_line)
        low_name_of_song = result[0].lower()
        result.remove(low_name_of_song)
        text_of_song = ''.join(result)
        execute("UPDATE song  SET low_name = ?, low_text = ? WHERE id = ?", (low_name_of_song, text_of_song, x))
        result.clear()

def update_text_of_song():
    result = []
    # max_id = execute("SELECT MAX(id) FROM song", [])
    # print(max_id)
    for x in range(1, 52):
        text = open(f"./text/text{x}.txt", "r", encoding="utf-8")
        for line in text:
            result.append(line)
        name_of_song = result[0]
        result.remove(name_of_song)
        text_of_song = ''.join(result)
        execute("UPDATE song SET text = ?, name = ? WHERE id = ?", (text_of_song, name_of_song, x))
        result.clear()

def import_image():
    last_line_number = execute("SELECT MAX(id) FROM song", [])[0]
    for x in range(1, last_line_number[0]+1):
        photo = open(f"./image/photo{x}.jpg", "rb")
        image = photo.read()
        execute("UPDATE song SET photo = ? WHERE id = ?", (image, x))

 #photo_id = record[0]
 #path = f"./image/photo{photo_id}.jpg"

# def search_song_infile(query):
#     results = []
#     for x in range(1, 34):
#         with open(f"./text/text{x}.txt", "r", encoding="utf-8") as f:
#             for line in f:
#                 if query.lower() in line.lower():
#                     results.append(line.strip())
#                     print(results)


#import_text_of_song()
#update_text_of_song()
# import_image()
# import_low_text_of_song()

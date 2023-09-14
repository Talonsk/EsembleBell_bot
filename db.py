import sqlite3


def execute(request, __parameters):
    conn = sqlite3.connect("SongBD.db")
    cursor = conn.cursor()
    cursor.execute(request, __parameters)
    conn.commit()
    cursor.close()
    conn.close()

def text_search(search):
    conn = sqlite3.connect('SongBD.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM song WHERE name LIKE '%" + search + "%' OR text LIKE '%" + search + "%'")
    found_text = cursor.fetchall()[0]
    cursor.close()
    conn.close()
    return found_text[0]

def upload_photo_song(name_of_song):
    conn = sqlite3.connect('SongBD.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, photo FROM song WHERE name LIKE '%" + name_of_song + "%'")
    record = cursor.fetchone()
    photo_id = record[0]
    photo = record[1]
    path = f"./image/photo{photo_id}.jpg"
    return photo


def download_song_text(name, text):
    execute("INSERT INTO song (name, text) VALUES (?, ?)", (name, text))

def delite_song_text(delit_name):
    execute('DELETE FROM song WHERE name = ?', [delit_name])

def update_song_text(update_text, update_name):
    execute("UPDATE song SET text = ? WHERE name = ?", (update_text, update_name))



#Загрузка текстов и изображений через файлы
def import_text_of_song():
    result = []
    for x in range(1, 34):
        text = open(f"./text/text{x}.txt", "r", encoding="utf-8")
        for line in text:
            result.append(line)
        name_of_song = result[0]
        result.remove(name_of_song)
        text_of_song = ''.join(result)
        execute("INSERT INTO song (name, text) VALUES (?, ?)", (name_of_song, text_of_song))
        result.clear()

def import_image():
    for x in range(1, 34):
        photo = open(f"./image/photo{x}.jpg", "rb")
        image = photo.read()
        execute("UPDATE song SET photo = ? WHERE id = ?", (image, x))

# def search_song_infile(query):
#     results = []
#     for x in range(1, 34):
#         with open(f"./text/text{x}.txt", "r", encoding="utf-8") as f:
#             for line in f:
#                 if query.lower() in line.lower():
#                     results.append(line.strip())
#                     print(results)


# import_text_of_song()
#import_image()

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
    if search != None:
        low_search = search.lower()
        search_wo_punctuation = low_search.translate(str.maketrans("", "", string.punctuation))
        new_search = '%'+search_wo_punctuation+'%'
        cursor.execute("SELECT id, text FROM song WHERE low_name LIKE ? OR low_text LIKE ?", [new_search, new_search])
        text = cursor.fetchall()
        # print(cursor.fetchall())
        found_text = text[0] #Первая из найденных пар айди:текст
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



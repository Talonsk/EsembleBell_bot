import os
import db
import string

#Загрузка текстов и изображений через файлы
def import_text_of_song():
    result = []
    max_id = db.execute("SELECT MAX(id) FROM song", [])[0][0]+1
    count_files = len(os.listdir('./text'))+1
    for x in range(max_id, count_files):
        text = open(f"./text/text{x}.txt", "r", encoding="utf-8")
        for line in text:
            result.append(line)
        name_of_song = result[0]
        result.remove(name_of_song)
        text_of_song = ''.join(result)
        db.execute("INSERT INTO song (name, text) VALUES (?, ?)", (name_of_song, text_of_song))
        result.clear()

def import_low_text_of_song():
    result = []
    count_files = len(os.listdir('./text'))+1
    for x in range(1, count_files):
        text = open(f"./text/text{x}.txt", "r", encoding="utf-8")
        for line in text:
            low_line = line.lower()
            new_line = low_line.translate(str.maketrans("", "", string.punctuation))
            result.append(new_line)
        low_name_of_song = result[0].lower()
        result.remove(low_name_of_song)
        text_of_song = ''.join(result)
        db.execute("UPDATE song  SET low_name = ?, low_text = ? WHERE id = ?", (low_name_of_song, text_of_song, x))
        result.clear()

def update_text_of_song():
    result = []
    max_id = db.execute("SELECT MAX(id) FROM song", [])[0][0]+1
    for x in range(1, max_id):
        text = open(f"./text/text{x}.txt", "r", encoding="utf-8")
        for line in text:
            result.append(line)
        name_of_song = result[0]
        result.remove(name_of_song)
        text_of_song = ''.join(result)
        db.execute("UPDATE song SET text = ?, name = ? WHERE id = ?", (text_of_song, name_of_song, x))
        result.clear()

def import_image():
    last_line_number = db.execute("SELECT MAX(id) FROM song", [])[0]
    for x in range(1, last_line_number[0]+1):
        photo = open(f"./image/photo{x}.jpg", "rb")
        image = photo.read()
        db.execute("UPDATE song SET photo = ? WHERE id = ?", (image, x))

def import_one_photo(song_id):
    photo = open("image.jpg", "rb")
    image = photo.read()
    db.execute("UPDATE song SET photo = ? WHERE id = ?", (image, song_id))

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


# import_text_of_song()
# update_text_of_song()
# import_image()
# import_low_text_of_song()


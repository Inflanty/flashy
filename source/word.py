# TABLE WORD
# WordID WordEN Sentence WordPL Category LectureID DikiLink
# require numpy==1.19.3 (pip install numpy==1.19.3)
import sqlite3
import csv


with open('l1.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    #for row in reader:
        #print(row)

newID = 1
origin = 'Bulb'
sentence = "The bulb is going to be broken tonight!"
trans = "żarówka"
category = "Home"
lectureID = 0
dikiLink = "https://www.diki.pl/slownik-angielskiego?q=bulb"

name = ':memory:'
conn = sqlite3.connect(str(name))
c = conn.cursor()
try :
    c.execute("""CREATE TABLE words (
        originID integer,
        origin text,
        sentence text,
        trans text,
        category text,
        lectureID integer,
        dikiLink text
        )""")
except sqlite3.OperationalError:
    print('Table words already exist!')

conn.commit()
name = 'words'
c.execute("INSERT INTO " + name + " VALUES (:originID, :origin, :sentence, :trans, :category, :lectureID, :dikiLink)",
    {'originID' : newID,
    'origin' : origin,
    'sentence' : sentence,
    'trans' : trans,
    'category' : category,
    'lectureID' : lectureID,
    'dikiLink' : dikiLink})
conn.commit()

newID = 2
origin = 'Sofa'
sentence = "I'm looking for a new sofa"
trans = "Sofa"
category = "HOME"
lectureID = 0
dikiLink = "https://www.diki.pl/slownik-angielskiego?q=sofa"

c.execute("INSERT INTO " + name + " VALUES (:originID, :origin, :sentence, :trans, :category, :lectureID, :dikiLink)",
    {'originID' : newID,
    'origin' : origin,
    'sentence' : sentence,
    'trans' : trans,
    'category' : category,
    'lectureID' : lectureID,
    'dikiLink' : dikiLink})
conn.commit()

c.execute("INSERT INTO " + name + " VALUES (:originID, :origin, :sentence, :trans, :category, :lectureID, :dikiLink)",
    {'originID' : newID + 1,
    'origin' : origin,
    'sentence' : sentence,
    'trans' : trans,
    'category' : category,
    'lectureID' : lectureID,
    'dikiLink' : dikiLink})
conn.commit()

c.execute("DELETE FROM " + name + " WHERE originID = " + str(2))
c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY 1;")
print(c.fetchall())

c.execute("select * from record")
print(c.fetchall())

conn.close()
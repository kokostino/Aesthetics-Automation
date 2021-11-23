import sqlite3

conn = sqlite3.connect('C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation\\database\\instagram.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IMAGE_INFO (
    IMAGE_NAME  TEXT NOT NULL PRIMARY KEY,
    IMAGE_COLOUR    TEXT,
    IMAGE_CLASS_SET    TEXT,
    IMAGE_CLASS_CALC    TEXT
);
''')
conn.commit()
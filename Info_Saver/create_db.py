import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path', help='path to database folder')
parser.add_argument('name', type=str, help='name of database file')
args = parser.parse_args()
db_file = args.path+'/'+args.name
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE projects
                  (ip text, project text, stage text,
                   update_time text, app text, verson text, build text, sha1 text)
               """)

conn.commit()
conn.close()
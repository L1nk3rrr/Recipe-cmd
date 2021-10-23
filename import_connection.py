import sqlite3, os
db_conn = sqlite3.connect("cooking.db")
c = db_conn.cursor()
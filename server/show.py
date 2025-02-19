import sqlite3


# Connect to the SQLite database
conn = sqlite3.connect('database/user.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM user_info")

users = cursor.fetchall()
print(users)

conn.close()



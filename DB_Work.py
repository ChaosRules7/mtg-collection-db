import mysql.connector
from datetime import datetime
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

now = datetime.now()
formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')

db = mysql.connector.connect(
    host=os.environ['IP'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database='testdb'
    )

mycursor = db.cursor()

example_data = [('User', hashlib.sha1(b'password').hexdigest(), formatted_time)]


# mycursor.executemany('INSERT INTO Users (login_name, pw_hash, date_created) VALUES (%s,%s,%s)', example_data)


# mycursor.execute('DELETE FROM Users WHERE login_name = "User"')


# mycursor.execute('ALTER TABLE Users CHANGE pw_hash pw_hash VARCHAR(100)')

# db.commit()

mycursor.execute('DESCRIBE Cards')
# single = mycursor.fetchone()

# print(single[0])
# print(hashlib.sha1(b'password').hexdigest())




for x in mycursor:
   print(x)



print(formatted_time)
import os, sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from connections.db import DB
import time
import datetime


def add_user(user_id, username, first_name, last_name):
    my_cursor = DB.cursor()
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    DB.autocommit = False
    try:
        sql = 'INSERT INTO Users (id, username, first_name, last_name, created_at, updated_at, deleted_at) '\
              'VALUES (%s, %s, %s, %s, %s, %s, %s)'

        val = (user_id, username, first_name, last_name, timestamp, timestamp, None)
        my_cursor.execute(sql, val)
        DB.commit()
    except Exception as e:
        DB.rollback()
    finally:
        sql = 'SELECT * FROM Users WHERE id=%s'
        val = [user_id]
        my_cursor.execute(sql, val)

        my_result = my_cursor.fetchone()
        my_cursor.close()
        return my_result


import os, sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from connections.db import DB
import time
import datetime


def get_state(user_id, chat_id) -> int:
    result = find_user_chat(user_id, chat_id)
    return -1 if result is None else int(result[2])


def user_chat_exists(user_id, chat_id) -> bool:
    result = find_user_chat(user_id, chat_id)
    return False if result is None else True


def find_user_chat(user_id, chat_id):
    my_cursor = DB.cursor()

    sql = 'SELECT * FROM Users_Chats WHERE user_id=%s AND chat_id=%s'
    val = [user_id, chat_id]
    my_cursor.execute(sql, val)

    my_result = my_cursor.fetchone()
    my_cursor.close()
    return my_result


def add_user_chat(user_id, chat_id, state, last_sticker):
    my_cursor = DB.cursor()
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    DB.autocommit = False
    try:
        sql = 'INSERT INTO Users_Chats (user_id, chat_id, state, last_sticker, created_at, updated_at, deleted_at) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s)'

        val = (user_id, chat_id, state, last_sticker, timestamp, timestamp, None)
        my_cursor.execute(sql, val)
        DB.commit()
    except Exception as e:
        print(e)
        DB.rollback()
    finally:
        sql = 'SELECT * FROM Users_Chats WHERE user_id=%s AND chat_id=%s'
        val = [user_id, chat_id]
        my_cursor.execute(sql, val)

        my_result = my_cursor.fetchone()
        my_cursor.close()
        return my_result


def change_user_chat(user_id, chat_id, state, last_sticker):
    my_cursor = DB.cursor()

    DB.autocommit = False
    try:
        sql = 'UPDATE Users_Chats SET state = %s, last_sticker = %s ' \
              'WHERE user_id=%s AND chat_id=%s'

        val = (state, last_sticker, user_id, chat_id)
        my_cursor.execute(sql, val)
        DB.commit()
    except Exception as e:
        print(e)
        DB.rollback()
    finally:
        sql = 'SELECT * FROM Users_Chats WHERE user_id=%s AND chat_id=%s'
        val = [user_id, chat_id]
        my_cursor.execute(sql, val)

        my_result = my_cursor.fetchone()
        my_cursor.close()
        return my_result

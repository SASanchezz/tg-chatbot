import os, sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from connections.db import DB
import time
import datetime


def sticker_exists(title) -> bool:
    result = find_sticker(title)
    return False if result is None else True


def find_all_stickers():
    my_cursor = DB.cursor()
    my_cursor.execute('SELECT * FROM Stickers')
    my_result = my_cursor.fetchall()
    my_cursor.close()
    return my_result


def find_sticker(title):
    my_cursor = DB.cursor()

    sql = 'SELECT * FROM Stickers WHERE title=%s'
    val = [title]
    my_cursor.execute(sql, val)

    my_result = my_cursor.fetchone()
    my_cursor.close()
    return my_result


def add_sticker(title, sticker_id):
    my_cursor = DB.cursor()
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    DB.autocommit = False
    try:
        sql = 'INSERT INTO Stickers (title, sticker_id, created_at, updated_at, deleted_at) '\
              'VALUES (%s, %s, %s, %s, %s)'

        val = (title, sticker_id, timestamp, timestamp, None)
        my_cursor.execute(sql, val)
        DB.commit()
    except Exception as e:
        print(e)
        DB.rollback()
    finally:
        sql = 'SELECT * FROM Stickers WHERE title=%s'
        val = [title]
        my_cursor.execute(sql, val)

        my_result = my_cursor.fetchone()
        my_cursor.close()
        return my_result

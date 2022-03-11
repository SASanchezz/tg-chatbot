import os, sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import mysql.connector
from config.db import *


def create_connection():
    connect_db = mysql.connector.connect(
        host=connection.get('host'),
        port=connection.get('port'),
        database='tg_chatbot',
        user=user,
        passwd=password,
        time_zone='+02:00'
    )
    return connect_db


DB = create_connection()

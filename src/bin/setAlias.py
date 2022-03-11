import os
import sys


global src


def create_alias():
        src = os.path.dirname(os.path.abspath(__file__))


create_alias()

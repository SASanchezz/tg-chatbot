import string
import random


def my_id(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

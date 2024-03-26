import random
import string
import secrets
from random import randint
from flask import g
import logging


import shortuuid


def generate_uuid():
    # length = 6
    # characters = string.ascii_letters + string.digits
    #
    # # Generate a random string of specified length
    # random_short_integer = random.randint(0, 100)
    #
    # return random_short_integer

    range_start = 10 ** (8 - 1)
    range_end = (10 ** 8) - 1
    return randint(range_start, range_end)
    # return str(su.random(length=8))



def generate_shortuuid(prefix: str) -> str:
    id = prefix + shortuuid.ShortUUID().random(length=5)
    return id




def get_request_id():
    return g.request_id



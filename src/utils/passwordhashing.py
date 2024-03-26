
from bcrypt import gensalt, hashpw


def _hash_password(plain_password):
    """
    function to hash the password
    """
    salt = gensalt()
    hashed_password = hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password
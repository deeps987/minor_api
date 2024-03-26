import logging

import pymysql
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
# from mysql import connector
from models import database
from exception import NotFound, CustomException, InvalidCredentials, DBException
# from models import Dbb
from bcrypt import checkpw, hashpw, gensalt

from models.database import DBConnection
from utils.config import queries, prompts, menu, inputs, constant
from utils.uuid_generator import get_request_id

logger = logging.getLogger("auth_business")

ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"
NO = "No"
YES = "Yes"
NOT_FOUND = "Not Found"
USER_NOT_FOUND = "User not found"
UNAUTHORIZED = "Unauthorised"
INVALID_CREDENTIALS = "Invalid credentials."


class Authentication:

    def __init__(self):
        self.db = DBConnection()

    def authenticate_credentials(self, data):
        try:
            username = data['username']
            password = data['password']
            value = self.authenticate_user(username, password)
            # print(value)
            if value is True:
                access_token = create_access_token(identity=[username], fresh=True)
                jti_access_token = get_jti(access_token)
                refresh_token = create_refresh_token(identity=[username])
                jti_refresh_token = get_jti(refresh_token)
                logger.info(f"[{get_request_id()}] : Valid login by user.")
                return {ACCESS_TOKEN: access_token, REFRESH_TOKEN: refresh_token, "message": "User logged in successfully."}
            if value == NO:
                raise CustomException(404, NOT_FOUND, USER_NOT_FOUND)
            if not value:
                logger.warning(f"[{get_request_id()}] : Invalid login by user.")
                raise CustomException(401, UNAUTHORIZED, INVALID_CREDENTIALS)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, "Internal Server Error", "Something wrong with the server.")

    def authenticate_user(self, user_name, password):
        db_password = Authentication().get_password_from_db(user_name)
        if db_password is None:
            print("hoo")
            return NO
        hashed_password_bytes = db_password.encode('utf-8')
        password_bytes = password.encode('utf-8') if db_password is not None else None
        if db_password is not None and checkpw(password_bytes, hashed_password_bytes):
            return True
        else:
            return False

    def get_password_from_db(self, user_name):
        db_password = self.db.get_item(queries["GET_PASSWORD"], (user_name,))
        return db_password[0] if db_password and db_password[0] is not None else None

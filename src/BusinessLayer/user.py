import logging

import pymysql
from bcrypt import gensalt, hashpw
from flask_jwt_extended import get_jwt_identity
# from mysql import connector

from exception import InternalError, DBException, CustomException
from models.database import DBConnection
from utils import print_table, passwordhashing
from utils.config import queries, prompts
# from exception import InternalError, AlreadyExists, RoleError, BadInput, CustomException, NotFound
from utils.constants import INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT, NOT_FOUND, NOT_FOUND_USER, FORBIDDEN, \
    NOT_ALLOWED, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE, INTERNAL_ERROR_FETCH, CONFLICT, USERNAME_TAKEN, SUCCESS, \
    USERNAME, MINUS_ONE, PASSWORD, PHONE, ADDRESS, ADMIN, DISTINCT, ALL, ONE, ZERO, CUSTOMER, SELLER

logger = logging.getLogger("user_business")




class User:

    def __init__(self, **details):
        self.user_id = details.get('User_id')
        self.username = details.get('Username')
        self.password = details.get('Password')
        self.role = details.get('Role')
        self.name = details.get('Name')
        self.phone = details.get('Phone')
        self.address = details.get('Address')
        self.city = details.get('City')
        self.state = details.get('State')
        self.pincode = details.get('Pincode')
        self.db = DBConnection()

    def update_account(self, user_id, data):
        try:
            if data is None:
                raise CustomException(422, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE)
            if USERNAME in data:
                response = User().check_user_exists(queries["USERNAME_EXISTS"], data['username'])
                if response == MINUS_ONE:
                    User(user_id=user_id).change_username(data['username'], user_id)
            if PASSWORD in data:
                salt = gensalt()
                hashed_password = hashpw(data['password'].encode('utf-8'), salt)
                User(user_id=user_id).change_password(hashed_password, user_id)
            if PHONE in data:
                User(user_id=user_id).change_phone(data['phone'], user_id)
            if ADDRESS in data:
                User(user_id=user_id).change_address(
                    (data['address'], data['city'], data['state'], data['pincode'], user_id))
            # if not username and not password and not phone and not address:
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)
            return SUCCESS
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, "Internal Server Error", "Something wrong with the server.")

    def change_password(self, hashed_password, user_id):
        """
        Function to change password
        """
        password = self.db.update_items(queries["UPDATE_PASSWORD"], hashed_password, user_id)
        return password

    def delete_account(self, jwt, username):
        """
        Function to delete account
        """
        try:
            response = User().check_user_exists(queries["USERNAME_EXISTS"], username)
            if response == MINUS_ONE:
                raise CustomException(404, NOT_FOUND, NOT_FOUND_USER)
            if jwt['role'] == ADMIN:
                self.db.remove_item(queries["CANCEL_PRODUCT_USERNAME"], username)
                self.db.remove_item(queries["REMOVE_PRODUCTS_USERNAME"], username)
                self.db.remove_item(queries["REMOVE_USER"], username)
                self.db.remove_item(queries["REMOVE_USER_AUTHENTICATE"], username)
                self.db.update_items(queries["UPDATE_REQUEST_TABLE"], username)
                # if not r1 or not r2 or not r3 or not r4 or not r5:
                #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)
                return SUCCESS
            raise CustomException(403, FORBIDDEN, NOT_ALLOWED)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, "Internal Server Error", "Something went wrong with the server.")

    def change_address(self, details):
        result = self.db.update_items(queries["UPDATE_ADDRESS"], *details)
        return result

    def change_phone(self, phone, user_id):
        result = self.db.update_items(queries["UPDATE_PHONE"], phone, user_id)
        return result

    def change_username(self, username, user_id):
        result = self.db.update_items(queries["UPDATE_USERNAME"], username, user_id)
        return result

    def view_unique_requests(self, jwt, value):
        try:
            if jwt['role'] != ADMIN:
                raise CustomException(403, FORBIDDEN, NOT_ALLOWED)
            if DISTINCT not in value and ALL not in value:
                raise CustomException(422, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE)
            data = self.db.get_items(queries["LIST_REQUESTS"], "PENDING")
            # if not data:
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)
            return data
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            return DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)

    def check_user_exists(self, query, username):
        response = self.db.check_item(query, username)
        if response > 0:
            return ONE
        elif response is False:
            return MINUS_ONE
        else:
            return ZERO

    def view_user(self, jwt, value):
        try:
            if value != CUSTOMER and value != SELLER:
                raise CustomException(422, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE)
            if jwt['role'] != ADMIN:
                raise CustomException(403, FORBIDDEN, NOT_ALLOWED)
            if CUSTOMER not in value and SELLER not in value:
                raise CustomException(422, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE)
            if value == CUSTOMER:
                detail = self.db.get_items(queries["GET_CUSTOMERS"])
            else:
                detail = self.db.get_items(queries["GET_SELLERS"])
            # if detail is False:
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_FETCH)
            details = []
            for d1 in detail:
                det = {"Name": d1[0], "Username": d1[1], "Phone": d1[2], "Address": d1[3], "City": d1[4],
                       "State": d1[5], "Pincode": d1[6]}
                details.append(det)
            return details
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise CustomException(500, INTERNAL_ERROR, INTERNAL_ERROR_FETCH)

    def get_role(self, username):
        result = self.db.get_items(queries["CHECK_ROLE"], username)
        return result

    def get_personal_details(self, user_id):
        try:
            details = self.db.get_items(queries["FETCH_DETAILS"], (user_id,))
            # if details is False:
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)
            return details
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)

    def add_user(self, data):
        try:
            hashed_password = passwordhashing._hash_password(data['password'])
            auth_details = [data['username'], hashed_password, data['role']]
            # new_user = [data['name'], data['phone'], data['address'], data['city'], data['state'], data['pincode'],
            #             data['username']]
            self.db.adduser(queries["ADD_AUTHENTICATE"], *auth_details)
            user_id = self.db.get_item("SELECT user_id FROM authenticate WHERE username = %s", (data['username'],))
            new_user = [user_id[0], data['name'], data['phone'], data['address'], data['city'], data['state'], data['pincode'],]
            self.db.adduser(queries["ADD_USER"], *new_user)
            return SUCCESS
        except pymysql.IntegrityError as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(409, CONFLICT, USERNAME_TAKEN)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, "Internal Server Error", "Something wrong with the server.")


    def request_delete_account(self, jwt):
        """
        Function for requesting to delete account(for sellers)
        """
        try:
            self.db.update_items(queries["REQUEST_DELETE"], get_jwt_identity()[0], "PENDING")
            return "Success"
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, "Internal Server Error", "Something wrong with the server.")

    # def view_requests(self):
    #     details = Dbb.get_items(queries["LIST_ALL_REQUESTS"])
    #     return details

    # def get_type(self, user_id):
    #     result = Dbb.get_items(queries["CHECK_TYPE"], user_id)
    #     return result[0][0]

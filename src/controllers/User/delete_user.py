import logging

from bcrypt import gensalt, hashpw
from flask import jsonify
from BusinessLayer.user import User
from exception import CustomException

logger = logging.getLogger('delete_user_controller')




class DeleteUser:

    @staticmethod
    def delete_seller(jwt, username):
        try:
            result = User().delete_account(jwt, username)
            return result
        except CustomException as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

    @staticmethod
    def request_delete(jwt):
        try:
            User().request_delete_account(jwt)
            response = {"message": "Request Submitted."}
            return jsonify(response), 201
        except CustomException as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

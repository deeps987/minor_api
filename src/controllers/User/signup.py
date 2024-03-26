import logging

from flask import jsonify

from BusinessLayer.user import User
from exception import CustomException, DBException

logger = logging.getLogger('signup_controller')


class SignUp:

    @staticmethod
    def signup(data):
        try:
            result = User().add_user(data)
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

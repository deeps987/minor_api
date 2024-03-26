import logging

from flask import jsonify
from flask_jwt_extended import get_jwt

from BusinessLayer.logout import Token
from exception import DBException, CustomException

logger = logging.getLogger('logout_user_controller')

class Logout:

    @staticmethod
    def logout():
        try:
            jwt = get_jwt()
            result = Token().revoke_token(jwt)
            if result is True:
                details = {"status": 204}
                return jsonify(details), 204
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

import logging

from flask import jsonify

from BusinessLayer.user import User

from exception import CustomException, DBException

logger = logging.getLogger('update_user_controller')



class UpdateUser:

    @staticmethod
    def update_account(user_id, data):
        try:
            result = User().update_account(user_id, data)
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

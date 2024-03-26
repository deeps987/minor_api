import logging
from flask import jsonify
from BusinessLayer.user import User
from exception import CustomException, DBException

logger = logging.getLogger('view_user_controller')




class UserAccount:

    @staticmethod
    def view_account(user_id):
        try:
            detail = User().get_personal_details(user_id)
            details = {
                "Name": detail[0][0],
                "Phone": detail[0][1],
                "Address": detail[0][2],
                "City": detail[0][3],
                "State": detail[0][4],
                "Pincode": detail[0][5]
            }
            return details
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

    @staticmethod
    def view_users(jwt, value):
        try:
            details = User().view_user(jwt, value)
            return details
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

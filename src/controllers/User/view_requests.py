import logging

from flask import jsonify

from BusinessLayer.user import User
from exception import CustomException, DBException

logger = logging.getLogger('view_requests_controller')


class Request:

    @staticmethod
    def view_requests(jwt, value):
        try:
            result = User().view_unique_requests(jwt, value)
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']



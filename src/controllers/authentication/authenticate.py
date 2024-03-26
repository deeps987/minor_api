import logging

from flask import jsonify

from BusinessLayer.authenticate import Authentication
from exception import CustomException, NotFound, DBException
from utils.uuid_generator import get_request_id

logger = logging.getLogger('login_controller')


class Auth:
    def login(self, data):
        try:
            result = Authentication().authenticate_credentials(data)
            logger.info(f"[{get_request_id()}] : User logged in successfully.")
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']


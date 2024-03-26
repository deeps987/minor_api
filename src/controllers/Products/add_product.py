import logging

from flask import jsonify

from BusinessLayer.product import Products
from exception import CustomException, DBException

logger = logging.getLogger('add_product_controller')


class AddProducts:

    @staticmethod
    def add_products(jwt, data):
        try:
            result = Products().add_product(jwt, data) #Success
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

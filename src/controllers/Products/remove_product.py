import logging

from flask import jsonify

from BusinessLayer.product import Products
from exception import CustomException, DBException

logger = logging.getLogger('remove_product_controller')

class RemoveProduct:

    @staticmethod
    def remove_product(jwt, id):
        try:
            result = Products().remove_product(jwt, id)
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

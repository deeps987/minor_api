import logging

from flask import jsonify

from BusinessLayer.product import Products
from exception import CustomException, DBException

logger = logging.getLogger('update_product_controller')



class UpdateProduct:

    @staticmethod
    def update_product(jwt, id, quantity):
        try:
            data = Products().update_product(jwt, id, quantity)
            return data
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

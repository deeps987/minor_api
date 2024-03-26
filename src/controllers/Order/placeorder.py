import logging

from flask import jsonify

from BusinessLayer.product import Products
from BusinessLayer.order import Order
from exception import CustomException, DBException

logger = logging.getLogger('place_order_controller')

class PlaceOrder:

    @staticmethod
    def place_order(product_id, jwt, data):
        try:
            data = Order().place_order(product_id, jwt, data)
            return data
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']


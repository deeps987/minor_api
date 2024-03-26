import logging

from flask import jsonify

from BusinessLayer.order import Order
from exception import CustomException, DBException

logger = logging.getLogger('cancel_order_controller')

class CancelOrder:

    @staticmethod
    def cancel_order(jwt, product_id):
        try:
            result = Order().cancel_order(jwt, product_id)
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']


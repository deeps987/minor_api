import logging

from flask import jsonify

from BusinessLayer.order import Order
from BusinessLayer.product import Products
from exception import CustomException, DBException

logger = logging.getLogger('view_order_controller')


class ViewOrder:

    @staticmethod
    def view_customer_order(jwt):
        try:
            result = Order().view_orders(jwt)
            results = {"My Orders": result}
            return jsonify(results)
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

    @staticmethod
    def view_seller_order(jwt):
        try:
            result = Order().view_seller_orders(jwt)
            return result
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']


    @staticmethod
    def view_ordered_products(jwt):
        try:
            products = Products().list_products(jwt)
            response = {"Orders": products}
            return jsonify(response), 200
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']



import logging

from flask import jsonify

from BusinessLayer.product import Products
from exception import CustomException, DBException

logger = logging.getLogger('view_product_controller')



class ViewProducts:

    @staticmethod
    def get_product_keyword(keyword):
        try:
            response = Products().get_product_through_keyword(keyword)
            return jsonify(response)
        except (CustomException, DBException) as err:
            if isinstance(err, CustomException):
                logger.error("Custom error handled {}".format(err.error))
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

    @staticmethod
    def get_product_price(keyword, price):
        try:
            response = Products().get_product_through_keyword(keyword, price)
            return jsonify(response)
        except (CustomException, DBException) as err:
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

    @staticmethod
    def get_product_gender(gender):
        try:
            result = Products().get_product_of_gender(gender)
            return jsonify(result)
        except (CustomException, DBException) as err:
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']

    @staticmethod
    def get_seller_products(jwt):
        try:
            result = Products().get_seller_ordered_products(jwt)
            results = {"products": result}
            return jsonify(results)
        except (CustomException, DBException) as err:
            details = {"status": err.code,
                       "error": err.error,
                       "message": err.message}
            return jsonify(details), details['status']




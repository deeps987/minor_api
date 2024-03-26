import logging
import random

import pymysql
from flask_jwt_extended import get_jwt, get_jwt_identity
# from mysql import connector

import models
from models.database import DBConnection
from utils.config import queries, prompts, menu, inputs, constant
from utils.constants import INTERNAL_ERROR_UPDATE, INTERNAL_ERROR, NOT_FOUND, NOT_FOUND_PRODUCT, \
    INTERNAL_ERROR_PLACE_ORDER, INTERNAL_ERROR_FETCH_ORDER, NOT_FOUND_ORDER, INTERNAL_ERROR_CANCEL_ORDER
from utils.uuid_generator import generate_uuid
from datetime import datetime
from BusinessLayer.product import Products
# from models.db import Database

from exception import InternalError, DoesNotExist, CustomException, NotFound, RoleError, DBException

logger = logging.getLogger("order_business")


class Order:

    def __init__(self):
        self.order_id = None
        self.db = DBConnection()

    def place_order(self, product_id, jwt, data):
        """
        Function to place order foe the given product
        """
        try:
            if not Products().check_product_id_exists(product_id):
                raise CustomException(404, NOT_FOUND, NOT_FOUND_PRODUCT)
            order_id = generate_uuid()
            seller_id = self.db.get_items("SELECT user_id FROM product WHERE product_id = %s", (product_id,))
            order_date = str(datetime.now().date())
            print(get_jwt_identity()[0])
            items = [order_id, int(jwt['user_id']), (get_jwt_identity())[0], seller_id[0][0], product_id, data['quantity'], constant["COD"],
                     constant["PENDING"], order_date]
            if self.db.update_items(queries["PLACE_ORDER"], *items):
                self.db.update_items(queries["NEW_QUANTITY"], data['quantity'], product_id)
                return 'Success'
            # raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_PLACE_ORDER)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_PLACE_ORDER)

    def view_orders(self, jwt):
        """
        Function to view all orders of the given user
        """
        try:
            query = queries["VIEW_CUSTOMER_ORDER"]
            order = self.db.get_items(query, [jwt['user_id']])
            if order is None:
                raise CustomException(404, NOT_FOUND, "No orders available.")
            orders = []
            for ord in order:
                o1 = {
                    "Order_id": ord[0], "Product_id": ord[4], "Quantity": ord[5], "Status": ord[7], "Order_Date": ord[8]
                }
                orders.append(o1)
            return orders
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_PLACE_ORDER)

    def view_seller_orders(self, jwt):
        """
        Function to view all orders of the given user
        """
        try:
            query = queries["VIEW_SELLER_ORDER"]
            order = self.db.get_items(query, jwt['user_id'])
            # if order is False:
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_FETCH_ORDER)
            if order is None:
                raise CustomException(404, NOT_FOUND, NOT_FOUND_ORDER)
            orders = []
            for ord in order:
                o1 = {
                    "Order_id": ord[0], "Username": ord[2], "Product_id": ord[4], "Quantity": ord[5], "Status": ord[7], "Order_Date": ord[8]
                }
                orders.append(o1)
            return orders
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_PLACE_ORDER)


    def cancel_order(self, jwt, product_id):
        """
        Function to cancel order of the given product
        """
        try:
            if not Products().check_product_id_exists(product_id):
                raise CustomException(404, NOT_FOUND, NOT_FOUND_ORDER)
            quantity = self.db.get_item(queries["GET_CANCELLED_QUANTITY"], [int(jwt['user_id'])])
            if quantity != None:
                self.db.update_items(queries["CANCEL_ORDER"], jwt['user_id'], int(product_id))
                self.db.update_items(queries["UPDATE_PRODUCT_CANCELLED"], int(quantity[0]), product_id)
                return "Success"
            raise CustomException(404, NOT_FOUND, NOT_FOUND_ORDER)
        except pymysql.IntegrityError as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(409, "Conflict", "No order id exists.")
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_CANCEL_ORDER)
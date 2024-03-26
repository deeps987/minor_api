import logging

import pymysql
# from mysql import connector

import models
from models.database import DBConnection
from utils.config import queries, prompts, menu, inputs, constant
# import src.models

from exception import InternalError, NotFound, CustomException, RoleError, AlreadyExists, InvalidParams, DBException
from utils.constants import CONFLICT, PRODUCT_ID_EXIST, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT, NOT_FOUND, \
    NOT_FOUND_PRODUCT, INTERNAL_ERROR_DELETE, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE, INTERNAL_ERROR_FETCH_PRODUCT, \
    NOT_FOUND_PRODUCT_KEYWORD, SUCCESS

logger = logging.getLogger("product_business")

HIGH = 'high'
LOW = 'low'
MEN = 'Men'
WOMEN = 'Women'
KIDS = 'Kids'


class Products:

    def __init__(self, **product_detail):
        self.product_id = product_detail.get('Product_id')
        self.seller_id = product_detail.get('Seller_id')
        self.description = product_detail.get('Description')
        self.keyword = product_detail.get('Keyword')
        self.category = product_detail.get('Category')
        self.gender = product_detail.get('Gender')
        self.price = product_detail.get('Price')
        self.size = product_detail.get('Size')
        self.quantity = product_detail.get('Quantity')
        self.db = DBConnection()

    def add_product(self, jwt, data):
        try:
            if Products().check_product_id_exists(data['product_id']):
                raise pymysql.IntegrityError
            items = [data['product_id'], jwt['user_id'], data['description'], data['price'], data['keyword'],
                     data['category'],
                     data['gender'], data['size'], data['quantity']]
            self.db.update_items(queries["ADD_PRODUCT"], *items)
            return SUCCESS
        except pymysql.IntegrityError as err:
            logger.error("{} occurred in Database".format(err))
            raise AlreadyExists(409, CONFLICT, PRODUCT_ID_EXIST)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)

    def remove_product(self, jwt, id):
        try:
            if not Products().check_product_id_exists(id):
                raise pymysql.IntegrityError
                # raise CustomException(404, NOT_FOUND, NOT_FOUND_PRODUCT)
            if self.db.remove_item(queries["REMOVE_PRODUCT"], id):
                self.db.update_items(queries["CANCEL_ORDER_PRODUCT"], id)
                return SUCCESS
            # raise InternalError(500, NOT_FOUND, NOT_FOUND_PRODUCT)
        except pymysql.IntegrityError as err:
            logger.error("{} occurred in Database".format(err))
            raise AlreadyExists(404, NOT_FOUND, NOT_FOUND_PRODUCT)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_DELETE)

    def check_product(self, product_id, user_id):
        """
        Function to check whether the product is present or not for that product_id
        """
        if self.db.check_item(queries["CHECK_PRODUCTID_EXISTS"], product_id, user_id):
            return True
        return False

    def update_product(self, jwt, product_id, quantity):
        """
        Function to update the quantity of product (only for sellers)
        """
        try:
            if not Products().check_product_id_exists(product_id):
                raise CustomException(404, NOT_FOUND, NOT_FOUND_PRODUCT)
            if not quantity['quantity'].isdigit():
                raise CustomException(422, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE)
            self.db.update_items(queries["UPDATE_PRODUCT"], int(quantity['quantity']), product_id)
            # if not result:
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)
            return SUCCESS
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)

    def get_product_of_gender(self, gender):
        """
        Function to get all Products for that gender
        """
        try:
            if gender != MEN and gender != WOMEN and gender != KIDS:
                raise CustomException(422, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE)
            product = self.db.get_items(queries["PRODUCTS"], (gender,))
            # if product is False:S
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)
            if product is None:
                raise NotFound(404, NOT_FOUND, NOT_FOUND_PRODUCT)
            products = []
            for pro in product:
                p1 = {'Product_id': pro[1], 'Description': pro[3], 'Price': pro[4], 'Category': pro[6],
                      'Gender': pro[7], 'Size': pro[8]}
                products.append(p1)
            return {"Products": products}
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)

    def check_product_keyword(self, keyword):
        """
        Function to check whether Products are available with that keyword or not
        """
        if self.db.check_item(queries["CHECK_KEYWORD_EXISTS"], keyword):
            return True
        return False

    def get_product_through_keyword(self, keyword, price=0):
        """
        Function to get all Products for that keyword
        """
        global product
        try:
            if price != 0:
                if price != LOW and price != HIGH:
                    raise CustomException(422, UNPROCESSABLE_ENTITY, VALID_PARAM_MESSAGE)
            if Products().check_product_keyword(keyword):
                if price == LOW:
                    product = self.db.get_items(queries["GET_PRODUCTS_WITH_KEYWORD_ASC"], (keyword, ))
                if price == HIGH:
                    product = self.db.get_items(queries["GET_PRODUCTS_WITH_KEYWORD_DESC"], (keyword, ))
                if price == 0:
                    product = self.db.get_items(queries["GET_PRODUCTS_WITH_KEYWORD"], (keyword,))
                products = []
                for pro in product:
                    p1 = {'Product_id': pro[1], 'Description': pro[3], 'Price': pro[4], 'Category': pro[6],
                          'Gender': pro[7], 'Size': pro[8]}
                    products.append(p1)
                return {"Products": products}
            raise CustomException(404, NOT_FOUND, NOT_FOUND_PRODUCT_KEYWORD)
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_FETCH_PRODUCT)

    def get_seller_ordered_products(self, jwt):
        """
        Function to get list of all the Products of the given seller which has been ordered at least once
        """
        try:
            user_id = jwt['user_id']
            product = self.db.get_items(queries["LIST_SELLER_PRODUCTS"], (user_id,))
            if product is None:
                raise CustomException(404, NOT_FOUND, NOT_FOUND_PRODUCT)
            products = []
            for pro in product:
                p1 = {'Product_id': pro[0], 'Description': pro[1], 'Price': pro[2], 'Keyword': pro[3], 'Category': pro[4],
                      'Gender': pro[5], 'Size': pro[6], 'Quantity': pro[7]}
                products.append(p1)
            return products
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_ADD_PRODUCT)


    def list_products(self, jwt):
        try:
            product = self.db.get_items(queries["LIST_PRODUCTS"], (jwt['user_id'],))
            if product is None:
                raise CustomException(404, NOT_FOUND, NOT_FOUND_PRODUCT )
            products = []
            for pro in product:
                p1 = {'Product_id': pro[4], 'Username': pro[2], 'Quantity': pro[5], 'Status': pro[7], 'Order date': pro[8]}
                products.append(p1)
            return products

        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise InternalError(500, INTERNAL_ERROR, "Some error occured while fetching the orderd products.")



    def check_product_id_exists(self, product_id):
        """
        Function to check whether the entered product id exist or not
        """
        if self.db.check_item(queries["PRODUCT_ID_EXISTS"], product_id):
            return True
        return False

    def check_quantity_exist(self, product_id):
        """
        Function to check whether the quantity entered by the customer for the given product is available or not
        """
        quantity = self.db.get_item(queries["CHECK_QUANTITY"], product_id)
        return quantity

    # @staticmethod
    # def get_product_details(user):
    #     """
    #     Function to get all the details about the given product
    #     """
    #     product = models.Dbb.get_items(queries["GET_PRODUCT_DETAILS"], user.user_id)
    #     return product

    # def list_products(self, user_id):
    #     products = models.Dbb.get_items(queries["LIST_PRODUCTS"], user_id)
    #     return products

    # product = Products()
    # products = product.list_products(user.user_id)
    # print_table.list_products(products)

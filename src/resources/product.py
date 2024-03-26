from flask import jsonify, request
from flask.views import MethodView
from flask import Request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_smorest import Blueprint, abort

from controllers.Products.remove_product import RemoveProduct
from controllers.Products.update_product import UpdateProduct
from controllers.Products.view_product import ViewProducts
from controllers.Products.add_product import AddProducts
from controllers.Order.placeorder import PlaceOrder
from schemas import ProductSchema, SellerSchema
from utils.role_based import role_required

blb = Blueprint("Product", "Products", description="Operations on Products")


@blb.route('/product')
class ProductFilter(MethodView):

    @blb.response(200, ProductSchema)
    def get(self):
        keyword = request.args.get('keyword')
        price = request.args.get('price')
        gender = request.args.get('gender')
        if keyword is not None and price is not None:
            details = ViewProducts.get_product_price(keyword, price)
            return details
        elif keyword is not None:
            details = ViewProducts.get_product_keyword(keyword)
            return details
        elif gender is not None:
            details = ViewProducts.get_product_gender(gender)
            return details
        # else:
        #     abort()



@blb.route('/products')
class SellerProducts(MethodView):

    @blb.response(200, ProductSchema)
    @role_required(["Seller"])
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        details = ViewProducts.get_seller_products(jwt)
        return details


    @blb.arguments(SellerSchema)
    @role_required(["Seller"])
    @jwt_required()
    def post(self, user_data):
        jwt = get_jwt()
        details = AddProducts.add_products(jwt, user_data)
        if details == "Success":
            return {"message": "Product added Successfully."}, 201
        return details


@blb.route(('/products/<product_id>'))
class DeleteOrPurchaseProduct(MethodView):


    @jwt_required()
    def post(self, product_id):
        jwt = get_jwt()
        data = request.get_json()
        details = PlaceOrder.place_order(product_id, jwt, data)
        if details == "Success":
            return {"message": "Order placed Successfully."}, 201
        return details


    @role_required(["Seller"])
    @jwt_required()
    def delete(self, product_id):
        jwt = get_jwt()
        details = RemoveProduct.remove_product(jwt, product_id)
        if details == 'Success':
            return {"message": "Product removed."}, 200
        return details

    @role_required(["Seller"])
    @jwt_required()
    def put(self, product_id):
        jwt = get_jwt()
        quantity = request.get_json()
        details = UpdateProduct.update_product(jwt, product_id, quantity)
        if details == 'Success':
            return {"message": "Product quantity updated."}, 200
        return details

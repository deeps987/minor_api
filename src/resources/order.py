from flask import jsonify, request
from flask.views import MethodView
from flask import Request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from controllers.Order.cancelorder import CancelOrder
from controllers.Order.vieworder import ViewOrder
from schemas import ProductSchema, OrderSchema
from utils.role_based import role_required

blb = Blueprint("Order", "Orders", description="Operations on Order")


@blb.route('/myorders')
class CustomerOrders(MethodView):

    @blb.response(200, OrderSchema)
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        details = ViewOrder.view_customer_order(jwt)
        print("DETAILS ",details)
        return details


# @blb.route('/orders')
# class SellerOrders(MethodView):
#
#     @blb.response(200, OrderSchema)
#     @role_required(["Seller"])
#     @jwt_required()
#     def get(self):
#         jwt = get_jwt()
#         details = ViewOrder.view_seller_order(jwt)
#         return details


@blb.route('/orders/<product_id>')
class CancelOrders(MethodView):

    @jwt_required()
    def post(self, product_id):
        jwt = get_jwt()
        details = CancelOrder.cancel_order(jwt, product_id)
        if details == "Success":
            return {"message": "Order cancelled Successfully."}, 200
        return details

@blb.route('/orders')
class ViewOrders(MethodView):

    @role_required(["Seller"])
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        response = ViewOrder.view_ordered_products(jwt)
        return response


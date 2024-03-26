from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_smorest import Blueprint, abort, response

from controllers.User.logout_controller import Logout
from controllers.User.signup import SignUp
from controllers.User.view_user import UserAccount
from controllers.User.update_user import UpdateUser
from controllers.User.delete_user import DeleteUser
from controllers.User.view_requests import Request
from schemas import UserSchema, UserResponseSchema, UserRequestSchema, UserDetailsSchema, UserUpdateSchema
from utils.role_based import role_required

blb = Blueprint("User", "user", description="Operations on user")





@blb.route('/signup')
class Signup(MethodView):

    @blb.arguments(UserSchema)
    def post(self, data):
        details = SignUp.signup(data)
        if details == 'Success':
            return {"message": "Account created successfully"}, 201
        return details


@blb.route('/account')
class User(MethodView):

    @blb.response(200, UserDetailsSchema)
    @jwt_required()
    def get(self):
        identity = get_jwt()
        details = UserAccount.view_account(identity['user_id'])
        return details

    @blb.arguments(UserUpdateSchema)
    @jwt_required()
    def put(self, data):
        identity = get_jwt()
        details = UpdateUser.update_account(identity['user_id'], data)
        if details == 'Success':
            return {"message": "Account updated Successfully."}, 200
        return details


@blb.route('/account/<username>')
class DeleteUsers(MethodView):

    @role_required(["Admin"])
    @jwt_required()
    def delete(self, username):
        jwt = get_jwt()
        details = DeleteUser.delete_seller(jwt, username)
        if details == 'Success':
            return {"message": "Account deleted successfully"}, 200
        return details


@blb.route('/users/<string:value>')
class ViewUsers(MethodView):

    @blb.response(200, UserResponseSchema)
    @role_required(["Admin"])
    @jwt_required()
    def get(self, value):
        jwt = get_jwt()
        details = UserAccount.view_users(jwt, value)
        return details

@blb.route('/requests')
class AddRequests(MethodView):

    @role_required(["Seller"])
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        details = DeleteUser.request_delete(jwt)
        return details

@blb.route('/requests/<string:value>')
class ViewRequests(MethodView):

    @blb.response(200, UserRequestSchema)
    @role_required(["Admin"])
    @jwt_required()
    def get(self, value):
        jwt = get_jwt()
        details = Request.view_requests(jwt, value)
        return details


@blb.route('/logout')
class LogOut(MethodView):

    @jwt_required()
    def post(self):
        details = Logout.logout()
        return details

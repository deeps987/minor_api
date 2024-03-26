import logging

from flask import jsonify

from controllers.authentication.authenticate import Auth
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AuthSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity

from utils.uuid_generator import get_request_id

logger = logging.getLogger("login")
blb = Blueprint("Login", "login", description="Operations on login")


@blb.route('/login')
class Authentication(MethodView):

    @blb.arguments(AuthSchema)
    def post(self, user_data):
        details = Auth().login(user_data)
        logger.info(f"[{get_request_id()}] : Login route accessed by user.")
        return details



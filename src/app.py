import logging

from flask_jwt_extended import JWTManager
from flask import Flask, jsonify, g
from flask_smorest import Api

from BusinessLayer.user import User

from resources.authenticate import blb as AuthBlueprint
from resources.user import blb as UserBlueprint
from resources.product import blb as ProductBlueprint
from resources.order import blb as OrderBlueprint
from utils.logout import initialise_jwt_config
from utils.uuid_generator import generate_shortuuid

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)-d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.log'
)
def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "Online Shopping REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['DEBUG'] = True

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "25339446708963499269000046428341264752"
    jwt = JWTManager(app)

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     result = User(user_id=identity).get_role(identity)
    #     # print(result)
    #     return {"role": result[0][0], "user_id": result[0][1]}

    initialise_jwt_config(app)

    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(OrderBlueprint)

    @app.before_request
    def get_request_id():
        new_request_id = generate_shortuuid("REQ")
        g.request_id = new_request_id
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)

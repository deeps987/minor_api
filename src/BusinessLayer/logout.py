# from models.database import Database
# from exception import InternalError, CustomException
import logging

import pymysql
# from mysql import connector

from exception import DBException
# from models import Dbb
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti

from models.database import DBConnection
from utils.constants import INTERNAL_ERROR, INTERNAL_ERROR_UPDATE

logger = logging.getLogger("logout_business")

REVOKED = "revoked"

class Token:

    def __init__(self):
        self.db = DBConnection()

    def check_token_revoked(self, jwt_payload):
        """check if token is revoked or not"""

        jti_access_token = jwt_payload.get('jti')
        result = self.db.get_item("""SELECT token_status FROM logout WHERE access_token = %s """, (jti_access_token,))
        if result is not None:
            result = result[0]
        if result == REVOKED:
            return True
        return False

    def revoke_token(self, jwt_payload):
        """To change the status of token to revoked"""
        try:
            jti_access_token = jwt_payload["jti"]
            self.db.update_items(""" UPDATE logout SET token_status = %s WHERE access_token = %s """, 'revoked', jti_access_token)
            # if not result:
            #     raise InternalError(500, INTERNAL_ERROR, INTERNAL_ERROR_UPDATE)
            return True
        except pymysql.Error as err:
            logger.error("{} occurred in Database".format(err))
            raise DBException(500, INTERNAL_ERROR, INTERNAL_ERROR_UPDATE)

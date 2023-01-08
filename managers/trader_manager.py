from constants.status_code import StatusCode
from dao.trader_dao import TraderDao
from http_handler.response_handler import ResponseHandler
from models.traders import TradersDB
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from object_storage import uploader_downloader

import logging

from dotenv import dotenv_values


# to handle the routes
class TraderManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = TraderDao()

    # insert new trader to the database
    def handle_trader(self, dt: dict):
        trader = TradersDB()
        trader.user_id = dt['user_id']
        trader.is_verified = dt.get('is_verified', False)
        trader.is_active = dt.get('is_active', True)
        trader.bio = dt['bio']

        try:
            self.dao.insert_new_trader(trader)
        except Exception as error:
            self.logger.error(ErrorMessage.TRADER_INSERT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()
        res.set_status_code(StatusCode.SUCCESS)
        return res

    # return the information of a trader
    def trader_detail(self, user_id):
        try:
            result = self.dao.select_trader(user_id)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception

        res = ResponseHandler()
        res.set_response({"message": result})
        res.set_status_code(StatusCode.SUCCESS)
        return res

    # update the information of an investor
    def trader_update(self, data: dict):
        try:
            self.dao.update_trader(data)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()
        res.set_status_code(StatusCode.SUCCESS)
        res.set_response({"message": InfoMessage.TRADER_UPDATE})

        return res


class Summarymanager:

    def __init__(self):
        self.config = dotenv_values(".env")
        self.obj_storage = uploader_downloader.Objectstorage(self.config["BUCKET_NAME"])
        self.logger = logging.getLogger(__name__)

    def uploader(self, user_id, raw_data):
        try:
            self.obj_storage.upload(user_id, raw_data)
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_INSERT)
            self.logger.error(error)

    def downloader(self, user_id):
        try:
            result = self.obj_storage.download(str(user_id))
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()
        res.set_response({"message": result})
        res.set_status_code(StatusCode.SUCCESS)
        return res

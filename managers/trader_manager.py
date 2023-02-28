from constants.status_code import StatusCode
from dao.trader_dao import TraderDao
from http_handler.response_handler import ResponseHandler
from models.traders import TradersDB
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from object_storage import uploader_downloader
from db.query_builder import QueryBuilder

import logging

from dotenv import dotenv_values


# to handle the routes
class TraderManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = TraderDao()
        self.db = QueryBuilder(self.config["TABLE_NAME"])

    # insert new trader to the database
    def handle_trader(self, dt: dict):
        trader = TradersDB()
        trader.user_id = dt.get('user_id', 'None')
        trader.is_verified = dt.get('is_verified', False)
        trader.is_active = dt.get('is_active', True)
        trader.bio = dt.get('bio', 'None')
        trader.api_key = dt.get('api_key', 'None')
        trader.secret_key = dt.get('secret_key', 'None')
        trader.exchange = dt.get('exchange', 'None')
        res = ResponseHandler()

        if all([trader.secret_key, trader.api_key, trader.exchange]):
            self.logger.error(ErrorMessage.BAD_REQUEST)
            res.set_status_code(StatusCode.BAD_REQUEST)
            res.set_response({"message": ErrorMessage.TRADER_REQUIRE})
            return res

        try:
            self.dao.insert_new_trader(trader)
        except Exception as error:
            self.logger.error(ErrorMessage.TRADER_INSERT)
            self.logger.error(error)
            raise Exception
        res.set_status_code(StatusCode.SUCCESS)
        res.set_response({"message": InfoMessage.TRADER_SUCCESS})

        return res

    # return the information of a trader
    def trader_detail(self, user_id):
        if user_id == 'all':
            try:
                result = self.db.select()
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
        else:
            try:
                result = self.dao.select_trader(user_id)
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
        dict_result = self.create_dict_from_postgres(result)
        if not dict_result:
            res = ResponseHandler()
            res.set_response(dict_result)
            res.set_status_code(StatusCode.NOT_FOUND)
            return res

        res = ResponseHandler()
        res.set_response(dict_result)
        res.set_status_code(StatusCode.SUCCESS)
        return res

    # update the information of an investor
    def trader_update(self, data: dict):
        try:
            result = self.dao.select_trader(data["user_id"])
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()

        if not result:
            self.logger.error(ErrorMessage.DB_SELECT)
            res.set_status_code(StatusCode.NOT_FOUND)
            res.set_response({"message": ErrorMessage.DB_SELECT})
            return res
        else:

            try:
                self.dao.update_trader(data)
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.TRADER_UPDATE})

            return res

    @staticmethod
    def create_dict_from_postgres(res):
        columns = ['id',
                   'user_id',
                   'is_verified',
                   'is_active'
                   'bio',
                   'api_key',
                   'exchange',
                   'secret_key',
                   'created_at',
                   'updated_at']
        results_list = []
        for ls in res:
            results_list.append({columns[i]: ls[i] for i in range(len(columns))})
        if len(results_list) == 1:
            results_list = results_list[0]
        return results_list


# to handle the routes
class TradeManager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.logger = logging.getLogger(__name__)
        self.dao = TraderDao()
        self.db = QueryBuilder("test_trader")

    # insert new trader to the database
    def handle_trader(self, dt: dict, user_id):
        trader = TradersDB()
        trader.user_id = user_id
        trader.is_verified = dt.get('is_verified', False)
        trader.is_active = dt.get('is_active', True)
        trader.bio = dt.get('bio')
        trader.api_key = dt.get('api_key')
        trader.secret_key = dt.get('secret_key')
        trader.exchange = dt.get('exchange')

        res = ResponseHandler()

        if all([trader.secret_key, trader.api_key, trader.exchange]):
            self.logger.error(ErrorMessage.BAD_REQUEST)
            res.set_status_code(StatusCode.BAD_REQUEST)
            res.set_response({"message": ErrorMessage.TRADER_REQUIRE})
            return res

        try:
            self.dao.insert_new_trader(trader)
        except Exception as error:
            self.logger.error(ErrorMessage.TRADER_INSERT)
            self.logger.error(error)
            raise Exception
        res.set_status_code(StatusCode.SUCCESS)
        res.set_response({"message": InfoMessage.TRADER_SUCCESS})

        return res

    # return the information of a trader
    def trader_detail(self, user_id):
        if user_id == 'all':
            try:
                result = self.db.select()
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
        else:
            try:
                result = self.dao.select_trader(user_id)
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
        dict_result = self.create_dict_from_postgres(result)
        res = ResponseHandler()
        res.set_response(dict_result)
        res.set_status_code(StatusCode.SUCCESS)
        return res

    # update the information of an investor
    def trader_update(self, data: dict, user_id):
        try:
            result = self.dao.select_trader(user_id)
        except Exception as error:
            self.logger.error(ErrorMessage.DB_SELECT)
            self.logger.error(error)
            raise Exception
        res = ResponseHandler()

        if not result:
            self.logger.error(ErrorMessage.DB_SELECT)
            res.set_status_code(StatusCode.NOT_FOUND)
            res.set_response({"message": ErrorMessage.DB_SELECT})
            return res
        else:

            try:
                self.dao.update_trader(data)
            except Exception as error:
                self.logger.error(ErrorMessage.DB_SELECT)
                self.logger.error(error)
                raise Exception
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.TRADER_UPDATE})

            return res

    @staticmethod
    def create_dict_from_postgres(res):
        columns = ['id',
                   'user_id',
                   'is_verified',
                   'is_active'
                   'bio',
                   'api_key',
                   'exchange',
                   'secret_key',
                   'created_at',
                   'updated_at']
        results_list = []
        for ls in res:
            results_list.append({columns[i]: ls[i] for i in range(len(columns))})
        if len(results_list) == 1:
            results_list = results_list[0]
        return results_list


class Miniomanager:
    def __init__(self):
        self.config = dotenv_values(".env")
        self.obj_storage = uploader_downloader.Objectstorage(self.config["BUCKET_NAME"])
        self.logger = logging.getLogger(__name__)

    def uploader(self, user_id, raw_data):
        res = ResponseHandler()
        try:
            self.obj_storage.upload(user_id, raw_data)
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.MINIO_INSERT})
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_INSERT)
            self.logger.error(error)
            res.set_status_code(StatusCode.INTERNAL_ERROR)
            res.set_response({"message": ErrorMessage.MINIO_INSERT})

        return res

    def downloader(self, user_id):
        try:
            self.obj_storage.download(user_id)
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_SELECT)
            self.logger.error(error)
            raise Exception

        return user_id


class Summarymanager:

    def __init__(self):
        self.config = dotenv_values(".env")
        self.obj_storage = uploader_downloader.Objectstorage(self.config["BUCKET_NAME"])
        self.logger = logging.getLogger(__name__)

    def uploader(self, user_id, raw_data):
        user_id_with_suffix = user_id + ".csv"
        res = ResponseHandler()
        try:
            self.obj_storage.upload(user_id_with_suffix, raw_data)
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.MINIO_INSERT})
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_INSERT)
            self.logger.error(error)
            res.set_status_code(StatusCode.INTERNAL_ERROR)
            res.set_response({"message": ErrorMessage.MINIO_INSERT})

        return res

    def downloader(self, user_id):
        user_id_with_suffix = user_id + ".csv"
        try:
            result = self.obj_storage.download(user_id_with_suffix)
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_SELECT)
            self.logger.error(error)
            raise Exception
        return user_id_with_suffix


class ResumeManager:

    def __init__(self):
        self.config = dotenv_values(".env")
        self.obj_storage = uploader_downloader.Objectstorage(self.config["BUCKET_NAME"])
        self.logger = logging.getLogger(__name__)

    def resume_uploader(self, user_id, raw_data):
        user_id = user_id + ".pdf"
        res = ResponseHandler()
        try:
            self.obj_storage.upload(user_id, raw_data)
            res.set_status_code(StatusCode.SUCCESS)
            res.set_response({"message": InfoMessage.MINIO_INSERT})
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_INSERT)
            self.logger.error(error)
            res.set_status_code(StatusCode.INTERNAL_ERROR)
            res.set_response({"message": ErrorMessage.MINIO_INSERT})
        return res

    def resume_downloader(self, user_id):
        user_id = user_id + ".pdf"

        try:
            result = self.obj_storage.download(user_id)
        except Exception as error:
            self.logger.error(ErrorMessage.MINIO_SELECT)
            self.logger.error(error)
            raise Exception
        return user_id

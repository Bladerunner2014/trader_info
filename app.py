import logging
from flask import Flask, request
from dotenv import dotenv_values

from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from blueprint import v1_blueprint
from object_storage.uploader_downloader import Objectstorage
from managers.trader_manager import TraderManager, Summarymanager
from swagger import swagger
from log import log

app = Flask("trader")
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


# To send information of a trader and store it to the database
@v1_blueprint.route('/trader', methods=['POST'])
def get_trader():
    request_data = request.get_json()
    trade_manager = TraderManager()
    if trade_manager.handle_trader(request_data):
        logger.info(InfoMessage.TRADER_SUCCESS)
    return InfoMessage.TRADER_SUCCESS, 200


# To get the information of a trader from database
@v1_blueprint.route('/trader/<string:user_id>', methods=['GET'])
def info_trader(user_id):
    if user_id is None:
        return logger.error(ErrorMessage.BAD_REQUEST)
    trade_detail = TraderManager()
    return trade_detail.trader_detail(user_id).generate_response()


# To update the information of a trader
@v1_blueprint.route("/trader", methods=["PUT"])
def update_trader():
    request_data = request.get_json()
    trader_manager = TraderManager()
    response = trader_manager.trader_update(request_data)
    return response.generate_response()


@v1_blueprint.route("/trader/upload", methods=["POST"])
def upload_summary_file():
    user_id = request.headers.get('user_id')
    raw_data = request.get_data()
    if len(raw_data) < 3:
        return 'badrequest', 300
    sum_manager = Summarymanager()
    sum_manager.uploader(user_id, raw_data)

    return 'ok', 200


@v1_blueprint.route("/trader/download", methods=["POST"])
def download_summary_file():
    user_id = request.headers.get('user_id')
    sum_manager = Summarymanager()
    if user_id is None:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return sum_manager.downloader(user_id).generate_response()


swagger.run_swagger(app)
log.setup_logger()

app.register_blueprint(v1_blueprint)
app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])

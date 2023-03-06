import logging
from flask import Flask, request
from constants.status_code import StatusCode
from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from blueprint import v2_blueprint, v1_blueprint
from managers.trader_manager import TraderManager, TradeManager, Miniomanager, Summarymanager, ResumeManager
from swagger import swagger
from log import log
from werkzeug.utils import secure_filename
from dotenv import dotenv_values
from http_handler.response_handler import ResponseHandler

app = Flask("trader")
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


def allowed_file(filename, user_id, allowed_extention: set):
    user_id = str(user_id)
    if '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extention:
        user_id += '.' + filename.rsplit('.', 1)[1].lower()
        return secure_filename(user_id)
    else:
        return False


# To send information of a trader and store it to the database
@v1_blueprint.route('/trader', methods=['POST'])
def get_trader():
    request_data = request.get_json()
    trade_manager = TraderManager()
    result = trade_manager.handle_trader(request_data)
    if result:
        logger.info(InfoMessage.TRADER_SUCCESS)
    return result.generate_response()


'''NOTE: if client send user_id == all, the endpoint below will return all of trader repo table'''


# To get the information of a trader from database
@v1_blueprint.route('/trader/<string:user_id>', methods=['GET'])
def info_trader(user_id):
    if user_id is None:
        return logger.error(ErrorMessage.BAD_REQUEST)
    trade_detail = TraderManager()
    result = trade_detail.trader_detail(user_id)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return result.generate_response()


@v1_blueprint.route('/trader/id/<string:user_id>', methods=['GET'])
def info_trader_by_id(user_id):
    if user_id is None:
        return logger.error(ErrorMessage.BAD_REQUEST)
    trade_detail = TraderManager()
    result = trade_detail.trader_detail_by_id(user_id)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return result.generate_response()


# To update the information of a trader
@v1_blueprint.route("/trader", methods=["PUT"])
def update_trader():
    request_data = request.get_json()
    trader_manager = TraderManager()
    response = trader_manager.trader_update(request_data)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return response.generate_response()


@v1_blueprint.route("/trader/upload", methods=["POST"])
def upload_summary_file():
    user_id = request.headers.get("user_id")
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    requested_file = request.files["file"]
    raw_data = requested_file.read()

    if not raw_data or not user_id:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    user_id_with_extension = allowed_file(filename=requested_file.filename, user_id=user_id,
                                          allowed_extention={'csv'})
    if not user_id_with_extension:
        logger.error(ErrorMessage.EXTENSION)
        return ErrorMessage.EXTENSION, StatusCode.BAD_REQUEST
    img_manager = Summarymanager()
    result = img_manager.uploader(user_id_with_extension, raw_data)
    if not result:

        return logger.error(ErrorMessage.BAD_REQUEST)

    return result.generate_response()


@v1_blueprint.route("/trader/download", methods=["POST"])
def download_summary_file():
    user_id = request.headers.get('user_id') + '.csv'
    if not user_id:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    sum_manager = Summarymanager()
    response = sum_manager.downloader(user_id)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return response.generate_response()


# For upload the trader resume file
@v1_blueprint.route("/trader/resume-upload", methods=["POST"])
def upload_resume_file():
    user_id = request.headers.get("user_id")
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    requested_file = request.files["file"]
    raw_data = requested_file.read()

    if not raw_data or not user_id:
        logger.error(ErrorMessage.BAD_REQUEST)
        return
    user_id_with_extension = allowed_file(filename=requested_file.filename, user_id=user_id,
                                          allowed_extention={'pdf'})
    if not user_id_with_extension:
        logger.error(ErrorMessage.EXTENSION)
        return ErrorMessage.EXTENSION, StatusCode.BAD_REQUEST
    img_manager = ResumeManager()
    result = img_manager.uploader(user_id_with_extension, raw_data)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return result.generate_response()


# For download the trader resume file
@v1_blueprint.route("/trader/resume-download", methods=["POST"])
def download_resume_file():
    user_id = request.headers.get('user_id') + '.pdf'
    if not user_id:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    sum_manager = ResumeManager()
    response = sum_manager.downloader(user_id)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return response.generate_response()


# To send information of a trader and store it to the database
@v2_blueprint.route('/trader', methods=['POST'])
def get_trader():
    user_id = request.headers.get('user_id')
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    request_data = request.get_json()
    trade_manager = TradeManager()
    result = trade_manager.handle_trader(request_data, user_id)
    if result:
        logger.info(InfoMessage.TRADER_SUCCESS)
    return result.generate_response()


'''NOTE: if client send user_id == all, the endpoint below will return all of trader repo table'''


# To get the information of a trader from database
@v2_blueprint.route('/trader', methods=['GET'])
def info_trader():
    user_id = request.headers.get('user_id')

    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    trade_detail = TradeManager()
    result = trade_detail.trader_detail(user_id)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return result.generate_response()


@v2_blueprint.route('/trader/id', methods=['GET'])
def info_trader_by_id():
    user_id = request.headers.get('user_id')
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    trade_detail = TraderManager()
    result = trade_detail.trader_detail_by_id(user_id)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return result.generate_response()


# To update the information of a trader
@v2_blueprint.route("/trader", methods=["PUT"])
def update_trader():
    user_id = request.headers.get('user_id')
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    request_data = request.get_json()
    trader_manager = TradeManager()
    response = trader_manager.trader_update(request_data, user_id)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)
    return response.generate_response()


@v2_blueprint.route("/trader/upload", methods=["POST"])
def upload_summary_file():
    user_id = request.headers.get("user_id")
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    requested_file = request.files["file"]
    raw_data = requested_file.read()

    if not raw_data or not user_id:
        return logger.error(ErrorMessage.BAD_REQUEST)
    user_id_with_extension = allowed_file(filename=requested_file.filename, user_id=user_id,
                                          allowed_extention={'csv'})
    if not user_id_with_extension:
        logger.error(ErrorMessage.EXTENSION)
        return ErrorMessage.EXTENSION, StatusCode.BAD_REQUEST
    img_manager = Miniomanager()
    result = img_manager.uploader(user_id_with_extension, raw_data)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return result.generate_response()


@v2_blueprint.route("/trader/download", methods=["GET"])
def download_summary_file():
    user_id = request.headers.get('user_id') + '.csv'
    if not user_id:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    sum_manager = Miniomanager()
    response = sum_manager.downloader(user_id)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return response.generate_response()


# For upload the trader resume file
@v2_blueprint.route("/trader/resume-upload", methods=["POST"])
def upload_resume_file():
    user_id = request.headers.get("user_id")
    if user_id is None:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    requested_file = request.files["file"]
    raw_data = requested_file.read()

    if not raw_data or not user_id:
        return logger.error(ErrorMessage.BAD_REQUEST)
    user_id_with_extension = allowed_file(filename=requested_file.filename, user_id=user_id,
                                          allowed_extention={'pdf'})
    if not user_id_with_extension:
        logger.error(ErrorMessage.EXTENSION)
        return ErrorMessage.EXTENSION, StatusCode.BAD_REQUEST
    img_manager = Miniomanager()
    result = img_manager.uploader(user_id_with_extension, raw_data)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return result.generate_response()


# For download the trader resume file
@v2_blueprint.route("/trader/resume-download", methods=["GET"])
def download_resume_file():
    user_id = request.headers.get('user_id') + '.pdf'
    if not user_id:
        logger.error(ErrorMessage.BAD_REQUEST)
        return ErrorMessage.BAD_REQUEST, StatusCode.BAD_REQUEST
    sum_manager = Miniomanager()
    response = sum_manager.downloader(user_id)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return response.generate_response()


swagger.run_swagger(app)
log.setup_logger()

app.register_blueprint(v2_blueprint)
app.register_blueprint(v1_blueprint)
app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])

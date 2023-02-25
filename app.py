import logging
from flask import Flask, request, send_from_directory
from dotenv import dotenv_values
import os

from constants.error_message import ErrorMessage
from constants.info_message import InfoMessage
from blueprint import v1_blueprint
from managers.trader_manager import TraderManager, Summarymanager, ResumeManager
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
    user_id = request.headers.get('user_id')
    print ('user_id')
    if not user_id:
        return logger.error(ErrorMessage.BAD_REQUEST)

    raw_data = request.get_data()
    if len(raw_data) < 3 or not user_id:
        return logger.error(ErrorMessage.BAD_REQUEST)
    sum_manager = Summarymanager()
    result = sum_manager.uploader(user_id, raw_data)
    print(result)
    if not result:
        return logger.error(ErrorMessage.BAD_REQUEST)

    return result.generate_response()


@v1_blueprint.route("/trader/download", methods=["POST"])
def download_summary_file():
    user_id = request.headers.get('user_id')
    if not user_id:
        return logger.error(ErrorMessage.BAD_REQUEST)
    sum_manager = Summarymanager()
    response = sum_manager.downloader(user_id)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)
    uploads = os.path.join(app.root_path, config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=response, as_attachment=True)


# For upload the trader resume file
@v1_blueprint.route("/trader/resume-upload", methods=["POST"])
def upload_resume_file():
    user_id = request.headers.get('user_id')

    if not user_id:
        return logger.error(ErrorMessage.BAD_REQUEST)

    raw_data = request.get_data()
    if len(raw_data) < 3:
        return 'badrequest', 300
    resume_manager = ResumeManager()
    response = resume_manager.resume_uploader(user_id, raw_data)

    return response.generate_response()


# For download the trader resume file
@v1_blueprint.route("/trader/resume-download", methods=["POST"])
def download_resume_file():
    user_id = request.headers.get('user_id')
    resume_manager = ResumeManager()
    if user_id is None:
        return logger.error(ErrorMessage.BAD_REQUEST)
    response = resume_manager.resume_downloader(user_id)
    if not response:
        return logger.error(ErrorMessage.BAD_REQUEST)

    uploads = os.path.join(app.root_path, config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=response, as_attachment=True)

swagger.run_swagger(app)
log.setup_logger()

app.register_blueprint(v1_blueprint)
app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])

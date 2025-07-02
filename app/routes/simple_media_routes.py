from flask import Blueprint
from ..controllers.simple_media_controller import SimpleMediaUploadController

simple_media_bp = Blueprint('simple_media', __name__, url_prefix='/upload')

controller = SimpleMediaUploadController()

@simple_media_bp.route('/file', methods=['POST'])
def upload_file():
    """API endpoint for single file upload"""
    return controller.upload_single_file()

@simple_media_bp.route('/popup', methods=['GET'])
def popup_uploader():
    """Popup uploader interface"""
    return controller.popup_uploader()

@simple_media_bp.route('/status', methods=['GET'])
def upload_status():
    """Get upload configuration"""
    return controller.get_upload_status()

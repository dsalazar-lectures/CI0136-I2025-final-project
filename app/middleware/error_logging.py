from functools import wraps
from flask import request, current_app
from app.services.audit import log_audit, AuditActionType
import traceback

def error_logging_middleware(app):

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Get the error details
        error_traceback = traceback.format_exc()
        error_message = str(e)
        
        # Log the error
        log_audit(
            "SYSTEM",
            AuditActionType.SYSTEM_ERROR,
            f"Error in {request.method} {request.path}: {error_message}\nTraceback: {error_traceback}"
        )
        
        # Re-raise the exception to let Flask handle it
        raise e 
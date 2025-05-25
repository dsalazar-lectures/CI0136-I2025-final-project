from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403
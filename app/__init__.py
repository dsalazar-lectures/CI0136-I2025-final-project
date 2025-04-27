from flask import Flask

def create_app():

    app = Flask(__name__)

    from .controllers.home import home as home_blueprint
    from .controllers.comments import comments_bp
    from .controllers.ratings import ratings_bp

    # Register blueprints
    app.register_blueprint(home_blueprint)
    app.register_blueprint(comments_bp)
    app.register_blueprint(ratings_bp, url_prefix='/comments')

    return app
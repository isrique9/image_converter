from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.main import bp as main_bp
    from app.routes.routes import bp as conversor_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(conversor_bp, url_prefix='/converter')
    return app
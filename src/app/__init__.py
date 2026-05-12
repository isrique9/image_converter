from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Apenas o blueprint principal que unifica upload + conversão
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)   # ele responde pela raiz '/'

    return app
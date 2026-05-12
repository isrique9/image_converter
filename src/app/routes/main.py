from datetime import datetime
import os
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    app_version = os.getenv('APP_VERSION', '')
    return render_template(
        'index.html',
        now=datetime.now(),
        app_version=app_version
    )
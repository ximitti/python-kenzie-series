from flask import Flask
from .views.views import register_series_views


# ----------------------------
def create_app() -> Flask:
    app = Flask(__name__)
    register_series_views(app)

    return app


# ----------------------------

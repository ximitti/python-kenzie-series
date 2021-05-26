from flask import Flask
from .views.views import register_series_views


# ----------------------------
app = Flask(__name__)

# ----------------------------
register_series_views(app)

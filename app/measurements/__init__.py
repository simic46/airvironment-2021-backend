from flask import Blueprint

measurements_bp = Blueprint('measurements_bp', __name__, url_prefix='/api/measurements')

import app.measurements.api

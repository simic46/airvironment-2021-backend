from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.measurements import models
from app.measurements.api import measurements

from app.measurements import measurements_bp

app.register_blueprint(measurements_bp)


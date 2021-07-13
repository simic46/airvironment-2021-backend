from app import app
from flask import render_template
from app import db
from app.models import Measurement

lista = [
        {
            "temperatura":24
        },
        {
            "temperatura":30
        },
        {
            "temperatura":40
        }
    ]



@app.route("/")
def hello_world():
    data = db.session.query(Measurement).all()
    return render_template("home.html", data=data)


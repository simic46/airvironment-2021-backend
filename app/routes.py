from app import app
from flask import render_template

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
    return render_template("home.html", lista=lista)


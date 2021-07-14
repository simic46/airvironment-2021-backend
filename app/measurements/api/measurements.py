from app import app
from flask import render_template
from app import db
from app.measurements.models import Measurement
from app.measurements import measurements_bp
import json
from flask import request
from app.measurements.constants import PAGE, PER_PAGE
from werkzeug.exceptions import NotFound


@measurements_bp.get('')
def get_all():
    page = int(request.args.get("page", PAGE))
    per_page = int(request.args.get("per_page", PER_PAGE))
    # all=request.args.get('all')
    #
    # if all=='123':
    #     return {"asdf" : 1}
    measurements = db.session.query(Measurement).paginate(per_page=per_page, page=page)

    response = {"meta": {"total" : measurements.total,
                         "page" : measurements.page,
                         "per_page" : measurements.per_page},
                "result" : []}

    # measurements = db.session.query(Measurement).all()
    #list_of_measurements = []
    #
    for measurement in measurements.items:
        data={"id": measurement.id,
              "temperature":measurement.temperature,
              "pollution":measurement.pollution,
              "humidity":measurement.humidity}

        response['result'].append(data)


    return json.dumps(response)


@measurements_bp.get('/<int:id>')
def get_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )
    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity
            }

    return json.dumps(data)


@measurements_bp.get('/latest')
def latest():

    measurement = db.session.query(Measurement).order_by(Measurement.id.desc()).first()

    if not measurement:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )
    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity
            }

    return data

@measurements_bp.post('')
def add():
    # data = {"id": request.body.id,
    #         "temperature": request.body.temperature,
    #         "pollution": request.body.pollution,
    #         "humidity": request.body.humidity
    #         }
    a = request.get_json()
    temp = int(a.get("temperature"))
    hum = int(a.get("humidity"))
    poll = int(a.get("pollution"))
    #import pdb; pdb.set_trace()

    measurement = Measurement(temp, hum, poll)
    db.session.add(measurement)
    db.session.commit()

    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity
            }

    return data



@measurements_bp.patch('/<int:id>')
def patch_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )

    a = request.get_json()
    import pdb;
    pdb.set_trace()

    if a.get("temperature"):
        measurement.temperature = int(a.get("temperature"))
    if a.get("humidity"):
        measurement.humidity = int(a.get("humidity"))
    if a.get("pollution"):
        measurement.pollution = int(a.get("pollution"))

    db.session.commit()

    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity
            }

    return data


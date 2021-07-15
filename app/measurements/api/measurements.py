from app import app
from flask import render_template
from app import db
from app.measurements.models import Measurement
from app.measurements import measurements_bp
import json
from flask import request
from app.measurements.constants import PAGE, PER_PAGE
from werkzeug.exceptions import NotFound
from app.measurements.schemas import MeasurementResponseSchema, MeasurementPostSchema, MeasurementPatchSchema, \
    MeasurementMetaSchema, MeasurementPaginationSchema
from pprint import pprint
from marshmallow import ValidationError

measurement_response_schema = MeasurementResponseSchema()
measurement_collection_response_schema = MeasurementResponseSchema(many=True)
measurement_post_schema = MeasurementPostSchema()
measurement_patch_schema = MeasurementPatchSchema()
measurement_meta_schema = MeasurementMetaSchema()
measurement_pagination_schema = MeasurementPaginationSchema()

@measurements_bp.get('')
def get_all():
    # page = int(request.args.get("page", PAGE))
    # per_page = int(request.args.get("per_page", PER_PAGE))
    # all=request.args.get('all')
    #
    # if all=='123':
    #     return {"asdf" : 1}
    schema_load = measurement_meta_schema.load(request.args.to_dict())
    measurements = db.session.query(Measurement).\
        paginate(per_page=schema_load.get('per_page'), page=schema_load.get('page'))

    # response = {"meta": {"total" : measurements.total,
    #                      "page" : measurements.page,
    #                      "per_page" : measurements.per_page},
    #             "result" : []}

    # measurements = db.session.query(Measurement).all()
    #list_of_measurements = []
    #
    # for measurement in measurements.items:
    #     data={"id": measurement.id,
    #           "temperature":measurement.temperature,
    #           "pollution":measurement.pollution,
    #           "humidity":measurement.humidity}
    #
    #     response['result'].append(data)
    #
    # return json.dumps(response)

    return measurement_pagination_schema.dump(measurements)


@measurements_bp.get('/<int:id>')
def get_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )

    return measurement_response_schema.dump(measurement) #iz baze nam prebaci podatke u JSON


@measurements_bp.get('/latest')
def latest():

    measurement = db.session.query(Measurement).order_by(Measurement.id.desc()).first()

    if not measurement:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )

    return measurement_response_schema.dump(measurement)


@measurements_bp.post('')
def add():

    post_data = measurement_post_schema.load(request.get_json())

    #import pdb; pdb.set_trace()

    measurement = Measurement(post_data.temperature, post_data.humidity, post_data.pollution)

    db.session.add(measurement)
    db.session.commit()

    return measurement_response_schema.dump(measurement)


@measurements_bp.patch('/<int:id>')
def patch_id(id):
    measurement = db.session.query(Measurement).filter(Measurement.id == id).one_or_none()

    if not measurement:
        return NotFound(
            description='Measurement with {} does not exist'.format(id)
        )

    a = measurement_patch_schema.load(request.get_json())
    # import pdb; pdb.set_trace()

    if a.get("temperature"):
        measurement.temperature = a.get("temperature")
    if a.get("humidity"):
        measurement.humidity = a.get("humidity")
    if a.get("pollution"):
        measurement.pollution = a.get("pollution")

    db.session.commit()

    return measurement_response_schema.dump(measurement)


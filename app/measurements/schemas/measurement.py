from marshmallow import Schema, fields, validate, EXCLUDE, pre_load, ValidationError, post_load
from app.measurements.view import MeasurementView
from app.measurements.constants import PAGE, PER_PAGE


class MeasurementResponseSchema(Schema):

    id = fields.Integer()
    temperature = fields.Float()
    pollution = fields.Float()
    humidity = fields.Float()
    created = fields.DateTime()


class MeasurementPostSchema(Schema):

    temperature = fields.Float(validate=validate.Range(min=0, max=50), required=True)
    pollution = fields.Float(validate=validate.Range(min=0, max=160), required=True)
    humidity = fields.Float(validate=validate.Range(min=0, max=100), required=True)

    @post_load()
    def test(self, data, **kwargs):
        return MeasurementView(**data)


class MeasurementPatchSchema(Schema):

    temperature = fields.Float(validate=validate.Range(min=0, max=50))
    pollution = fields.Float(validate=validate.Range(min=0, max=160))
    humidity = fields.Float(validate=validate.Range(min=0, max=100))

    # @pre_load()
    # def test(self, data):
    #     if 'temperature' not in data:
    #         raise ValidationError('something')


class MeasurementMetaSchema(Schema):
    page = fields.Integer(required=False, deafult=PER_PAGE, missing=PAGE)
    pollution = fields.Integer(required=False, missing=PER_PAGE, default=PAGE)
    humidity = fields.Integer(required=False, missing=0, default=0)


class MeasurementPaginationSchema(Schema):
    meta = fields.Method('get_meta')
    response = fields.Method('get_results')

    @staticmethod
    def get_meta(data):
        response = dict()
        response["total"] = data.total
        response["page"] = data.page
        response["per_page"] = data.per_page
        return MeasurementMetaSchema().dump(response)

    @staticmethod
    def get_results(data):
        return MeasurementResponseSchema(many=True).dump(data.items)

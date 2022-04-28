from marshmallow import fields, validates, ValidationError

from schemas.base import BaseSchema


class Vehicle(BaseSchema):
    id = fields.Int(required=True, allow_none=False)
    start_index = fields.Int(required=True, allow_none=False)
    capacity = fields.List(fields.Int, required=False,
                           allow_none=True, default=[])


class Job(BaseSchema):
    id = fields.Int(required=True, allow_none=False)
    location_index = fields.Int(required=True, allow_none=False)
    delivery = fields.List(
        fields.Int, required=False,
        allow_none=True, default=[]
    )
    service = fields.Int(required=False, allow_none=True)


class RoutesRequestSchema(BaseSchema):
    vehicles = fields.List(fields.Nested(Vehicle), required=True)
    jobs = fields.List(fields.Nested(Job), required=True)
    matrix = fields.List(fields.List(fields.Int,  # duration_matrix
                                     required=True,
                                     allow_none=False),
                         required=True,
                         allow_none=False)

    @validates('vehicles')
    def __vehicles(self, value):
        if not value:
            raise ValidationError("Can't be an empty list!")

    @validates('jobs')
    def __jobs(self, value):
        if not value:
            raise ValidationError("Can't be an empty list!")

    @validates('matrix')
    def __matrix(self, value):
        if not value:
            raise ValidationError("Can't be an empty list!")

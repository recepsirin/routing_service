from marshmallow import fields

from schemas.base import BaseSchema


class Route(BaseSchema):
    jobs = fields.List(fields.Str, default=[])
    delivery_duration = fields.Int(required=True, allow_none=False, default=0)


class RoutesResponseSchema(BaseSchema):
    total_delivery_duration = fields.Int(required=True, allow_none=False,
                                         default=0)
    routes = fields.Dict(value=fields.Nested(Route), many=True)


"""
    routes = fields.Dict(fields.Dict(keys=fields.String(),
                                     values=fields.Nested(Route),
                                     many=True))
    
"""

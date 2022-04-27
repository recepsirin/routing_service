from marshmallow import fields

from base import BaseSchema


class RouteItem(BaseSchema):
    jobs = fields.Dict(
        fields.List(fields.Str),
        required=False,
        allow_none=True,
        default=[]
    )
    delivery_duration = fields.Int(required=True, allow_none=False, default=0)


class Route(BaseSchema):
    route = fields.Dict(fields.Nested(RouteItem,
                                      required=True,
                                      allow_none=False))


class AlgorithmResponse(BaseSchema):
    total_delivery_duration = fields.Int(required=True, allow_none=False)
    routes = fields.Dict(fields.Nested(Route))

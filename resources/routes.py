import json

from flask_restful import Resource
from flask import Response, request

from models.algorithm_input import AlgorithmInput
from models.routes import Routes
from schemas.routes_request import RoutesRequestSchema
from schemas.routes_response import RoutesResponseSchema
from services.algorithm import AlgorithmService
from openrouteservice.exceptions import ApiError


class RouteResource(Resource):
    def __init__(self):
        self._routes_request_schema = RoutesRequestSchema()
        self._algorithm_service = AlgorithmService()

    def post(self):
        payload = request.get_json(force=True)
        schema = self._routes_request_schema.validate(payload)
        if schema:
            return Response(json.dumps(schema), status=400,
                            mimetype='application/json')
        serialized_data = self._routes_request_schema.serialize(payload)
        AlgorithmInput(vehicles=serialized_data['vehicles'],
                       jobs=serialized_data['jobs'],
                       matrix=serialized_data['matrix']).save()
        routes = self._algorithm_service.calculate_routes(serialized_data)
        if isinstance(routes, ApiError):
            return Response(routes.__str__(), status=routes.status,
                            mimetype='application/json')
        Routes(total_delivery_duration=routes['total_delivery_duration'],
               routes=routes['routes']).save()
        return Response(json.dumps(RoutesResponseSchema().deserialize(routes)),
                        status=201,
                        mimetype='application/json'
                        )

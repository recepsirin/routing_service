import json

from flask_restful import Resource
from flask import Response, request

from schemas.algorithm_request import AlgorithmRequestSchema


class RouteResource(Resource):
    def __init__(self):
        self._algorithm_request_schema = AlgorithmRequestSchema()

    def post(self):
        payload = request.get_json(force=True)
        schema = self._algorithm_request_schema.validate(payload)

        if schema:
            return Response(json.dumps(schema), status=400,
                            mimetype='application/json')
        serialized_data = self._algorithm_request_schema.serialize(payload)
        vehicles = serialized_data['vehicles']
        jobs = serialized_data['jobs']
        matrix = serialized_data['matrix']
        pass



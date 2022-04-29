import json

from app import app, api, initialize_endpoints
from tests.base import BaseTestCase


class TestRoutesEndpoint(BaseTestCase):
    def setUp(self):
        super(TestRoutesEndpoint, self).setUp()
        app.config['TESTING'] = True
        initialize_endpoints(api)  # @TODO Replace this
        self.client = app.test_client()

    def _make_success_request(self):
        payload = self.read_mock_data("validated_input")
        response = self.client.post("/api/v1/routes",
                                    json={
                                        "vehicles": payload['vehicles'],
                                        "jobs": payload['jobs'],
                                        "matrix": payload['matrix']
                                    },
                                    headers={
                                        "Content-Type": "application/json"})
        return response

    def test_post_success(self):
        response = self._make_success_request()
        self.assertEqual(201, response.status_code)

    def test_response_validation(self):
        response = self._make_success_request()
        response = json.loads(response.data)
        routes = self.read_mock_data("validated_routes")
        self.assertEqual(response, routes)
        self.assertIn("routes", response)
        self.assertIn("total_delivery_duration", response)
        self.assertIn("jobs", response['routes']["1"])
        self.assertIn("delivery_duration", response['routes']["1"])

    def test_request_validation(self):
        # @TODO Implement It
        pass

    def test_algorithm_recursion_causes_bad_request(self):
        # @TODO Implement It
        pass

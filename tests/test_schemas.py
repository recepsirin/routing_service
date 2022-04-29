from schemas.routes_request import RoutesRequestSchema
from schemas.routes_response import RoutesResponseSchema
from tests.base import BaseTestCase


class TestRoutesRequestSchema(BaseTestCase):

    def setUp(self):
        self.schema = RoutesRequestSchema()

    def create_schema(self):
        request_schema_data = self.read_mock_data("validated_input")
        return request_schema_data

    def test_serializing(self):
        data = self.create_schema()
        self.assertIsInstance(self.schema.serialize(data), dict)
        self.assertIn("vehicles", self.schema.serialize(data))
        self.assertIn("jobs", self.schema.serialize(data))
        self.assertIn("matrix", self.schema.serialize(data))

    def test_deserializing(self):
        data = self.create_schema()
        self.assertIsInstance(self.schema.deserialize(data), dict)
        self.assertIn("vehicles", self.schema.deserialize(data))
        self.assertIn("jobs", self.schema.deserialize(data))
        self.assertIn("matrix", self.schema.deserialize(data))

    def test_validation(self):
        data = self.create_schema()
        self.assertIsInstance(self.schema.validate(data), dict)
        self.assertDictEqual(self.schema.validate(data), {})


class TestRoutesResponseSchema(BaseTestCase):

    def setUp(self):
        self.schema = RoutesResponseSchema()

    def create_schema(self):
        response_schema_data = self.read_mock_data("validated_routes")
        return response_schema_data

    def test_serializing(self):
        data = self.create_schema()
        self.assertIsInstance(self.schema.serialize(data), dict)
        self.assertIn("total_delivery_duration", self.schema.serialize(data))
        self.assertIn("routes", self.schema.serialize(data))
        self.assertIn("jobs", self.schema.serialize(data)['routes']['1'])
        self.assertIn("delivery_duration",
                      self.schema.serialize(data)['routes']['1'])

    def test_deserializing(self):
        data = self.create_schema()
        self.assertIsInstance(self.schema.deserialize(data), dict)
        self.assertIn("total_delivery_duration", self.schema.deserialize(data))
        self.assertIn("routes", self.schema.deserialize(data))
        self.assertIn("jobs", self.schema.deserialize(data)['routes']['1'])
        self.assertIn("delivery_duration",
                      self.schema.deserialize(data)['routes']['1'])

    def test_validation(self):
        data = self.create_schema()
        self.assertIsInstance(self.schema.validate(data), dict)
        self.assertDictEqual(self.schema.validate(data), {})

# @TODO Add more tests

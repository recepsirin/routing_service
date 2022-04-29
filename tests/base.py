import json
import os
from unittest import TestCase
from mongoengine import connect, disconnect


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://mongo:27017')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    @staticmethod
    def read_mock_data(filename):
        filename = filename + ".json"
        with open(os.path.join("tests/mock_data/", filename)) as f:
            return json.load(f)

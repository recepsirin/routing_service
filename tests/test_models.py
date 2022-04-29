from mongoengine import ValidationError

from models.routes import Routes, Route
from tests.base import BaseTestCase
from models.algorithm_input import AlgorithmInput, Vehicle, Job


class TestAlgorithmInputModel(BaseTestCase):

    def test_validation_ok(self):
        # NOQA  python -m unittest tests.test_models.TestAlgorithmInputModel.test_validation_ok
        validated_input = self.read_mock_data("validated_input")
        algo_input = AlgorithmInput(vehicles=validated_input['vehicles'],
                                    jobs=validated_input['jobs'],
                                    matrix=validated_input['matrix'])
        algo_input.validate()
        algo_input.save()

        qs = AlgorithmInput.objects.first()
        # @TODO Needs Refactor: separate validation & type comparison
        self.assertEqual(len(qs.vehicles), len(validated_input['vehicles']))
        self.assertIsInstance(qs.vehicles[0], Vehicle)
        self.assertEqual(len(qs.jobs), len(validated_input['jobs']))
        self.assertIsInstance(qs.jobs[0], Job)
        self.assertEqual(qs.vehicles[0].start_index,
                         validated_input['vehicles'][0]['start_index'])
        self.assertEqual(qs.jobs[0].location_index,
                         validated_input['jobs'][0]['location_index'])
        self.assertIsInstance(validated_input['matrix'][0], list)
        self.assertIsInstance(validated_input['matrix'][0][0], int)

    def test_validation_error(self):
        # NOQA  python -m unittest tests.test_models.TestAlgorithmInputModel.test_validation_error
        invalidated_input = self.read_mock_data("invalidated_input")
        algo_input = AlgorithmInput(vehicles=invalidated_input['vehicles'],
                                    jobs=invalidated_input['jobs'],
                                    matrix=invalidated_input['matrix'])
        with self.assertRaises(ValidationError):
            algo_input.validate()


class TestRoutesModel(BaseTestCase):

    def _create_test_object(self):
        routes_data = self.read_mock_data("validated_routes")
        routes = Routes(**routes_data)
        routes.validate()
        routes.save()
        qs = Routes.objects.first()
        return qs, routes_data

    def test_validation_ok(self):
        self._create_test_object()

    def test_model_types(self):
        qs, data = self._create_test_object()
        print(qs['routes']['1'], type(qs['routes']['1']))
        self.assertIsInstance(qs['total_delivery_duration'], int)
        self.assertIsInstance(qs['routes'], dict)
        self.assertIsInstance(qs['routes']['1'], dict)
        self.assertIsInstance(qs['routes']['1']['jobs'], list)
        self.assertNotIsInstance(qs['routes']['1'], Route)
        self.assertIsInstance(qs, Routes)
        self.assertEqual(len(qs.routes), len(data['routes']))
        self.assertEqual(qs.routes['1']['jobs'][0],
                         data['routes']['1']['jobs'][0])
        self.assertEqual(qs.total_delivery_duration,
                         data['total_delivery_duration'])
        self.assertNotEqual(qs.routes['1']['delivery_duration'],
                            data['routes']['2']['delivery_duration'])

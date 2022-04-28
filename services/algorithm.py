import logging
from abc import ABC, abstractmethod

from openrouteservice import Client
from openrouteservice.optimization import Vehicle, Job

from utils import config_parser


class BaseRouteOptimizer(ABC):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def parse(self, data):
        pass


class ORSOptimizer(BaseRouteOptimizer):
    """
    ORS optimization API
    Vehicle Routing Problem with Roaming Delivery Location and
    Stochastic Travel Times (VRPRDL-S)
    """

    def __init__(self, vrp_inputs, timeout=60, retry_timeout=60):
        __api_key = config_parser()['solver']['APIs']['openrouteservice'][
            'key']
        self._client = Client(key=__api_key,
                              timeout=timeout,
                              retry_timeout=retry_timeout)
        self.inputs = vrp_inputs

    @property
    def vehicles(self):
        if all([i.get('capacity') for i in self.inputs['vehicles']]):
            return [Vehicle(id=v['id'], start_index=v['start_index'],
                            capacity=v['capacity'])
                    for v in self.inputs['vehicles']]
        return [Vehicle(id=v['id'], start_index=v['start_index'])
                for v in self.inputs['vehicles']]

    @property
    def jobs(self):
        if all([i.get('service') for i in self.inputs['jobs']]):
            return [Job(id=j['id'], location_index=j['location_index'],
                        service=j['service']) for j in self.inputs['jobs']]
        return [Job(id=j['id'], location_index=j['location_index'])
                for j in self.inputs['jobs']]

    @property
    def duration_matrix(self):
        return self.inputs['matrix']

    def run(self):
        try:
            response = self._client.optimization(jobs=self.jobs,
                                                 vehicles=self.vehicles,
                                                 matrix=self.duration_matrix)
        except Exception as e:
            logging.exception(e)
            return e
        parsed_response = self.parse(response)
        convenient_data = self.set_empty_routes(
            vehicles=self.inputs['vehicles'],
            routes=parsed_response)
        return convenient_data

    def parse(self, response):
        parsed_data = dict()
        parsed_data['total_delivery_duration'] = response['summary'][
            'duration']
        parsed_data['routes'] = {}

        for route in response['routes']:
            parsed_data['routes'][str(route['vehicle'])] = {}
            parsed_data['routes'][str(route['vehicle'])]['jobs'] = []
            parsed_data['routes'][str(route['vehicle'])]['delivery_duration'] \
                = route['duration']
            for job in route['steps']:
                if job['type'] == "job":
                    parsed_data['routes'][str(route['vehicle'])][
                        'jobs'].append(str(job['id']))
        return parsed_data

    @staticmethod
    def set_empty_routes(vehicles, routes):
        """Sets empty routes for API's response convenience"""
        for v in vehicles:
            if not str(v['id']) in routes['routes']:
                routes['routes'][str(v['id'])] = {
                    "jobs": [],
                    "delivery_duration": 0
                }
        return routes


class Algorithms(object):
    ors = ORSOptimizer  # consumes openrouteservice's api
    # other algorithms/solvers/optimizers here: cvrp, vrptw and etc..


class AlgorithmService(object):

    def calculate_routes(self, algorithm_inputs, algorithm="ors"):
        _algo_cls_obj = self.__get_an_algorithm(algorithm_inputs, algorithm)
        return _algo_cls_obj.run()

    @classmethod
    def __get_an_algorithm(cls, inputs, algorithm):
        _algo_obj = getattr(Algorithms, algorithm)(cls)
        return _algo_obj.__class__(inputs)

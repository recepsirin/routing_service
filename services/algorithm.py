import logging
from abc import ABC, abstractmethod
from urllib.error import HTTPError

from openrouteservice import Client
from openrouteservice.optimization import Vehicle, Job


class BaseAlgorithm(ABC):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def parse(self, data):
        pass


class Solution1(BaseAlgorithm):
    # @TODO Apply naming convention
    """
    Vehicle Routing Problem with Roaming Delivery Location and
    Stochastic Travel Times (VRPRDL-S)
    """

    def __init__(self, vrp_inputs, timeout=60, retry_timeout=60):
        self._client = Client("key", timeout=timeout,
                              retry_timeout=retry_timeout)
        self.inputs = vrp_inputs

    @property
    def vehicles(self):
        return [Vehicle(id=v['id'], start_index=v['start_index'],
                        capacity=v['capacity'])
                for v in self.inputs['vehicles']]

    @property
    def jobs(self):
        return [Job(id=j['id'], location_index=j['location_index'],
                    service=j['service']) for j in self.inputs['jobs']]

    @property
    def duration_matrix(self):
        return self.inputs['matrix']

    def run(self):
        try:
            response = self._client.optimization(jobs=self.jobs,
                                                 vehicles=self.vehicles,
                                                 matrix=self.duration_matrix)
        except HTTPError as err:
            # Todo Customize error-handling for HTTP Errors
            # err.code 400 sent missing/improper data
            logging.exception(err)
            raise err
        except Exception as e:
            logging.exception(e)
            raise e
        parsed_response = self.parse(response)
        # @ TODO set_empty_routes
        return parsed_response

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

    def set_empty_routes(self, vehicles, routes):
        pass


class AlgorithmService(object):
    pass

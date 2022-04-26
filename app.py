import logging
import yaml
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
db = MongoEngine()


def __parser():
    config = dict()
    with open("config.yml", 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            logging.error(exc)
    return config


def initialize_app_config(app):
    app.config['TESTING'] = __parser()['TESTING']
    app.config['DEBUG'] = __parser()['DEBUG']
    app.config['MONGODB_SETTINGS'] = {
        'host': __parser()['database']['mongo']['dsn']
    }
    app.config['MONGODB_DB'] = __parser()['database']['mongo']['name']


def initialize_db(app):
    db.init_app(app)


def initialize_endpoints(api):
    """Since we do have only one resource, we do not need to be structured
    url-routes but versioning"""
    version = "/api/v1/"  # representative
    resource = "routes"  # resource
    from resources.routes import RouteResource
    api.add_resource(RouteResource, version+resource)


def initialize():
    initialize_app_config(app)
    initialize_db(app)
    initialize_endpoints(api)


def start_app():
    initialize()
    app.run()


if __name__ == '__main__':
    start_app()

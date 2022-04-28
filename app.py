from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

from utils import config_parser

app = Flask(__name__)
api = Api(app)
db = MongoEngine()


def initialize_app_config(app):
    app.config['TESTING'] = config_parser()['TESTING']
    app.config['DEBUG'] = config_parser()['DEBUG']
    app.config['MONGODB_SETTINGS'] = {
        'host': config_parser()['database']['mongo']['dsn']
    }
    app.config['MONGODB_DB'] = config_parser()['database']['mongo']['name']


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

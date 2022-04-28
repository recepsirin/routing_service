from flask_mongoengine import Document
from mongoengine import (IntField, ListField, DictField, EmbeddedDocumentField,
                         StringField, EmbeddedDocument)


class RouteItem(EmbeddedDocument):
    jobs = DictField(ListField(StringField, required=False, default=[]))
    delivery_duration = IntField(required=True)


class Route(EmbeddedDocument):
    route = DictField(EmbeddedDocumentField(RouteItem), required=True)


class Routes(Document):
    total_delivery_duration = IntField(required=True)
    routes = DictField(EmbeddedDocumentField(Route), required=True)


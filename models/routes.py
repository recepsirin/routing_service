from flask_mongoengine import Document
from mongoengine import (IntField, ListField, DictField, EmbeddedDocumentField,
                         StringField, EmbeddedDocument)


class Route(EmbeddedDocument):
    jobs = ListField(StringField, required=False, default=[])
    delivery_duration = IntField(required=False, default=0)


class Routes(Document):
    total_delivery_duration = IntField(required=True, default=0)
    routes = DictField(value=EmbeddedDocumentField(Route), required=True)

from flask_mongoengine import Document
from mongoengine import (IntField, ListField, EmbeddedDocumentField,
                         EmbeddedDocument)


class Vehicle(EmbeddedDocument):
    start_index = IntField(required=True)
    capacity = ListField(required=False)


class Job(EmbeddedDocument):
    location_index = IntField(required=True)
    delivery = ListField(required=False)
    service = IntField(required=False)


class DurationMatrix(EmbeddedDocument):
    duration_matrix = ListField(EmbeddedDocumentField(ListField,
                                                      required=True),
                                required=True)


class AlgorithmInput(Document):
    vehicles = ListField(EmbeddedDocumentField(Vehicle))
    jobs = ListField(EmbeddedDocumentField(Job))
    matrix = ListField(EmbeddedDocumentField(DurationMatrix))

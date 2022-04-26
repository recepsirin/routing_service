from marshmallow import Schema


class BaseSchema(Schema):

    def serialize(self, payload):
        result = self.dump(payload)
        return result

    def deserialize(self, payload):
        result = self.load(payload)
        return result

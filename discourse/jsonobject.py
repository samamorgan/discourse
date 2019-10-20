import json


class JsonObject:
    """An object constructed from a JSON response"""

    def __init__(self, json):
        self.update_attributes(json)

    def __str__(self):
        return "{} with ID: {}".format(self.__class__.__name__, self.id)

    def __repr__(self):
        try:
            as_json = json.dumps(self.__dict__)
        except TypeError:
            as_json = "<invalid JSON>"
        return "{}(json={})".format(self.__class__.__name__, as_json)

    def update_attributes(self, json):
        self.__dict__.update(json)

class JsonObject:
    """An object constructed from a JSON response"""

    def __init__(self, json):
        self._data = json

    def __getattribute__(self, name):
        if name != "_data" and name in self._data:
            return self.json[name]

        return super().__getattribute__(name)

    def __str__(self):
        return "{} with ID: {}".format(self.__class__.__name__, self.id)

    def __repr__(self):
        return "{}(json={})".format(self.__class__.__name__, repr(self._data))

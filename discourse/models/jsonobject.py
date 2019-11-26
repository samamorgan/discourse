class JsonObject:
    """An object constructed from a JSON response"""

    def __init__(self, client, json):
        self.client = client
        self.update_attributes(json)

    def __repr__(self):
        # FIXME: This fails eval()
        vars_string = str(self.__dict__)

        replace = {": ": "=", "{": "", "}": ""}
        for key in replace:
            vars_string = vars_string.replace(key, replace[key])

        return "{}({})".format(self.__class__.__name__, vars_string)

    def __str__(self):
        return "{} with ID: {}".format(self.__class__.__name__, self.id)

    def update_attributes(self, json):
        self.__dict__.update(json)

    def json(self):
        d = self.__dict__
        del d["client"]
        return d

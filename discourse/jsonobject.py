class JsonObject(object):

    def __init__(self, json):
        self.__dict__.update(json)

import json

class JsonObject(object):

    def __init__(self, d):
        self.__dict__.update(d)

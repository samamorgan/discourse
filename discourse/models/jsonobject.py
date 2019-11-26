class JSONObject:
    """An object constructed from a JSON response"""

    def __init__(self, session, **kwargs):
        super().__init__()
        self._update(**kwargs)

    def __str__(self):
        try:
            return "{} with ID: {}".format(self.__class__.__name__, self.id)
        except AttributeError:
            return repr(self)

    def _update(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

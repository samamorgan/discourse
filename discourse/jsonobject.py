class JsonObject(object):
    '''An object constructed from a JSON response'''

    def __init__(self, json):
        self.update_attributes(json)

    def __str__(self):
        return '{} with ID: {}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        vars_string = str(self.__dict__)

        replace = {': ': '=', '{': '', '}': ''}
        for key in replace:
            vars_string = vars_string.replace(key, replace[key])

        return '{}({})'.format(self.__class__.__name__, vars_string)

    def update_attributes(self, json):
        self.__dict__.update(json)

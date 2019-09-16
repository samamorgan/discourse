class JsonObject(object):

    def __init__(self, json):
        self.__dict__.update(json)

    def __str__(self):
        return '{} #{}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        vars_string = str(vars(self))

        replace = {': ': '=', '{': '', '}': ''}
        for key in replace:
            vars_string = vars_string.replace(key, replace[key])

        return '{}({})'.format(self.__class__.__name__, vars_string)

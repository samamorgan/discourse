from .jsonobject import JsonObject


class Site(JsonObject):

    def __init__(self, client, **kwargs):
        # Want to initialize with as much data from the site as possible
        # IIRC site.json has this information. May use site_settings.json
        self.client = client

        super().__init__(**kwargs)

    # All site settings calls should go here

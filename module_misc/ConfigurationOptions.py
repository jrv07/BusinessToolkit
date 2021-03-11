class ConfigurationOptions:
    def __init__(self, tags: dict = None, skip_tags: dict = None, extra_variables: dict = None):
        self._tags = tags or {}
        self._skip_tags = skip_tags or {}
        self._extra_variables = extra_variables or {}

    @property
    def tags(self):
        return self._tags

    @property
    def skip_tags(self):
        return self._skip_tags

    @property
    def extra_variables(self):
        return self._extra_variables



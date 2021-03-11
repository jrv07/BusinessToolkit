import logging
import inspect


class Extraction:
    def __init__(self, key, specifier=None, optional=True, default=None, alternative=None, description=""):
        self._key = key
        if specifier is None:
            self._specifier = key
        else:
            self._specifier = specifier
        self._optional = optional
        self._description = description
        self._alternative = alternative
        self._default = default
        self._do_not_extract = False

    @property
    def key(self):
        return self._key

    @property
    def specifier(self):
        return self._specifier

    @property
    def alternative(self):
        return self._alternative

    @property
    def do_not_extract(self):
        return self._do_not_extract

    @do_not_extract.setter
    def do_not_extract(self, value):
        self._do_not_extract = value

    def check_optional(self, parameters):
        if not self._optional:
            if self._default is not None:
                return
            if self._alternative is not None:
                return
            logging.error('inside "{}", parameter "{}" is not optional and was NOT found.'
                          'Parameters: "{}"'
                          .format(inspect.stack()[0][3], self._specifier, parameters))
            raise ValueError

    def extract_specific(self, parameters, value):
        raise NotImplementedError

    def get_structure(self):
        structure = {}
        if self._specifier is not None:
            structure["specifier"] = self._specifier
        if self._key is not None:
            structure["key"] = self._key
        if self._optional is not None:
            structure["optional"] = self._optional
        if self._default is not None:
            structure["default"] = self._default
        if self._alternative is not None:
            structure["alternative"] = self._alternative
        if self._description is not None:
            structure["description"] = self._description
        return structure

    def extract(self, parameters):
        if parameters is None:
            return None
        if self._specifier in parameters:
            field_value = parameters[self._specifier]
            return self.extract_specific(parameters, field_value)
        self.check_optional(parameters)
        if self._default is not None:
            return self._default
        return None

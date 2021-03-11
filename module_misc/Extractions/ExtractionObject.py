from module_misc.Extractions.Extraction import Extraction
import logging
import inspect


class ExtractionObject(Extraction):
    def __init__(self, key, object_type, specifier=None, optional=True, alternative=None, description=""):
        super().__init__(key, specifier=specifier, optional=optional, alternative=alternative, description=description)
        self._object_type = object_type

    @property
    def object_type(self):
        return self._object_type

    def extract_specific(self, parameters, value):
        if not isinstance(value, dict):
            if self._alternative is None:
                logging.error('inside "{}", parameter "{}" must be a valid input for {}.'
                              ' Current value "{}". Parameters: "{}"'
                              .format(inspect.stack()[0][3], self._specifier, self._object_type, value, parameters))
                raise TypeError
            else:
                return None
        return value

    def get_structure(self):
        structure = super().get_structure()
        structure["is_list"] = False
        if self._object_type is not None:
            structure["type"] = self._object_type.__name__
        return structure

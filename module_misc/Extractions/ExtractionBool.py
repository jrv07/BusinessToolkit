from module_misc.Extractions.Extraction import Extraction
import logging
import inspect


class ExtractionBool(Extraction):
    def __init__(self, key, specifier=None, optional=True, default=None, alternative=None, description=""):
        super().__init__(key, specifier=specifier, optional=optional, default=default, alternative=alternative,
                         description=description)

    def extract_specific(self, parameters, value):
        if not isinstance(value, bool):
            logging.error('inside "{}", parameter "{}" must be a boolean value,'
                          ' eg True. Current value "{}". Parameters: "{}"'
                          .format(inspect.stack()[0][3], self._specifier, value, parameters))
            raise TypeError
        return value

    def get_structure(self):
        structure = super().get_structure()
        structure["is_list"] = False
        structure["type"] = bool.__name__
        return structure

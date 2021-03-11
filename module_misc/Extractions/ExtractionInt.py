from module_misc.Extractions.Extraction import Extraction
import logging
import inspect


class ExtractionInt(Extraction):
    def __init__(self, key, specifier=None, optional=True, default=None, alternative=None, description=""):
        super().__init__(key, specifier=specifier, optional=optional, default=default, alternative=alternative,
                         description=description)

    def extract_specific(self, parameters, value):
        try:
            parsed_value = int(value)
        except Exception as exception:
            if self._alternative is None:
                logging.error('inside "{}", parameter "{}" must be an integer value,'
                              ' eg 12. Current value "{}". Parameters: "{}"'
                              .format(inspect.stack()[0][3], self._specifier, value, parameters))
                raise TypeError
            else:
                return None
        return parsed_value

    def get_structure(self):
        structure = super().get_structure()
        structure["is_list"] = False
        structure["type"] = int.__name__
        return structure

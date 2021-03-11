from module_misc.Extractions.Extraction import Extraction
import logging
import inspect


class ExtractionStr(Extraction):
    def __init__(self, key, specifier=None, valid_values=None, optional=True, default=None, alternative=None,
                 description=""):
        super().__init__(key, specifier=specifier, optional=optional, default=default, alternative=alternative,
                         description=description)
        self._valid_values = valid_values

    def extract_specific(self, parameters, value):
        if not isinstance(value, str):
            if self._alternative is None:
                logging.error('inside "{}", parameter "{}" must be a string value,'
                              ' Current value "{}". Parameters: "{}"'
                              .format(inspect.stack()[0][3], self._specifier, value, parameters))
                raise TypeError
            else:
                return None
        if self._valid_values is not None and value not in self._valid_values:
            logging.error('inside "{}", parameter "{}" must be one of these values: "{}",'
                          ' Current value "{}". Parameters: "{}"'
                          .format(inspect.stack()[0][3], self._specifier, ", ".join(self._valid_values), value,
                                  parameters))
            raise ValueError
        return value

    def get_structure(self):
        structure = super().get_structure()
        structure["is_list"] = False
        structure["type"] = str.__name__
        if self._valid_values is not None:
            structure["valid_values"] = self._valid_values
        return structure

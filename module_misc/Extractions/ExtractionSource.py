from module_misc.Extractions.Extraction import Extraction
import logging
import inspect


class ExtractionSource(Extraction):
    def __init__(self, key, specifier=None, source_type=None, optional=True, alternative=None, is_dominant=False,
                 description=""):
        super().__init__(key, specifier=specifier, optional=optional, alternative=alternative, description=description)
        self._source_type = source_type
        self._is_dominant = is_dominant

    @property
    def source_type(self):
        return self._source_type

    @source_type.setter
    def source_type(self, value):
        self._source_type = value

    @property
    def is_dominant(self):
        return self._is_dominant

    def check_source_type(self, object_to_check):
        if not isinstance(object_to_check, self._source_type):
            if issubclass(type(object_to_check), self._source_type):
                return True
            return False
        return True

    def extract_specific(self, parameters, value):
        from share_objects import register
        if type(value) != str:
            if self._alternative is None:
                log_string = 'inside "{}", parameter "{}" must be a variable. Current value: {}. Parameters: {}' \
                    .format(inspect.stack()[0][3], self._specifier, value, parameters)
                logging.error(log_string)
                raise TypeError
            else:
                return None

        if self._source_type is not None:
            if not self.check_source_type(register[value]):
                if self._alternative is None:
                    log_string = 'inside "{}", parameter "{}" must be a {}. Current type "{}". Parameters: {}' \
                        .format(inspect.stack()[0][3], self._specifier, self._source_type.__name__, type(register[value]),
                                parameters)
                    logging.error(log_string)
                    raise TypeError
                else:
                    return None
        return register[value]

    def get_structure(self):
        structure = super().get_structure()
        structure["is_list"] = False
        if self._source_type is not None:
            structure["source_type"] = self._source_type.__name__
        if self._is_dominant is not None:
            structure["is_dominant"] = self._is_dominant
        return structure

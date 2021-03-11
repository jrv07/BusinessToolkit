from module_misc.Extractions.Extraction import Extraction
import logging
import inspect


class ExtractionList(Extraction):
    def __init__(self, key, specifier=None, entry_type=None, entry_object_type=None, length=None, min_length=None,
                 valid_values=None, optional=True, default=None, alternative=None, description=""):
        super().__init__(key, specifier=specifier, optional=optional, default=default, alternative=alternative,
                         description=description)
        self._entry_type = entry_type
        self._entry_object_type = entry_object_type
        if self._entry_object_type is None:
            self._entry_object_type = self._entry_type
        self._length = length
        self._min_length = min_length
        self._valid_values = valid_values

    @property
    def entry_type(self):
        return self._entry_type

    @property
    def entry_object_type(self):
        return self._entry_object_type

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

    @property
    def min_length(self):
        return self._min_length

    @min_length.setter
    def min_length(self, value):
        self._min_length = value

    @property
    def valid_values(self):
        return self._valid_values

    def get_log_message(self, parameters, field_value):
        if self._entry_type is None:
            if self._length is None:
                if self._min_length is None:
                    specific = "a list"
                else:
                    specific = "a list of at least {} values".format(self._min_length)
            else:
                specific = "a list of {} values".format(self._length)
        else:
            if self._length is None:
                if self._min_length is None:
                    specific = "a list of {} values".format(str(self._entry_type))
                else:
                    specific = "a list of at least {} {} values".format(self._min_length, str(self._entry_type))
            else:
                specific = "a list of {} {} values".format(self._length, str(self._entry_type))
        valid_values = ""
        if self._valid_values is not None:
            valid_values = " Valid values: [{}].".format(", ".join(self._valid_values))
        return 'inside "{}", parameter "{}" must be {}.{} Current value: {}. Parameters: {}'\
            .format(inspect.stack()[0][3], self._specifier, specific, valid_values, field_value, parameters)

    def check_list_type(self, field_value, log_msg) -> bool:
        if not isinstance(field_value, list):
            if self._alternative is None:
                logging.error(log_msg)
                raise TypeError
            else:
                return False
        return True

    def check_length(self, field_value, log_msg):
        if self._length is not None:
            if len(field_value) != self._length:
                logging.error(log_msg)
                raise ValueError

    def check_min_length(self, field_value, log_msg):
        if self._min_length is not None:
            if len(field_value) < self._min_length:
                logging.error(log_msg)
                raise ValueError

    def parse_entries(self, field_value, log_msg):
        if self._entry_type is not None:
            parsed_values = []
            for entry in field_value:
                if self._entry_type in [int, float]:
                    try:
                        parsed_entry = self._entry_type(entry)
                        parsed_values.append(parsed_entry)
                    except ValueError:
                        logging.error(log_msg)
                        raise TypeError
                else:
                    if not isinstance(entry, self._entry_type):
                        logging.error(log_msg)
                        raise TypeError
                    else:
                        parsed_values.append(entry)
        else:
            parsed_values = field_value
        return parsed_values

    def check_valid_values(self, field_value, log_msg):
        if self._valid_values is not None:
            for value in field_value:
                if value not in self._valid_values:
                    logging.error(log_msg)
                    raise ValueError

    def extract_specific(self, parameters, value):
        log_msg = self.get_log_message(parameters, value)
        if not self.check_list_type(value, log_msg):
            return None
        self.check_length(value, log_msg)
        self.check_min_length(value, log_msg)
        parsed_field_value = self.parse_entries(value, log_msg)
        self.check_valid_values(parsed_field_value, log_msg)
        return parsed_field_value

    def get_structure(self):
        structure = super().get_structure()
        structure["is_list"] = True
        structure["type"] = self._entry_object_type.__name__
        if self._length is not None:
            structure["length"] = self._length
        if self._min_length is not None:
            structure["min_length"] = self._min_length
        if self._valid_values is not None:
            structure["valid_values"] = self._valid_values
        return structure

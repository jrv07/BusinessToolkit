from module_misc.Extractions.ExtractionStr import ExtractionStr
from module_misc.Extractions.ExtractionBool import ExtractionBool
from module_misc.Extractions.ExtractionObject import ExtractionObject
from module_misc.Extractions.ExtractionList import ExtractionList
from module_misc.Extractions.ExtractionInt import ExtractionInt
from module_misc.Extractions.ExtractionFloat import ExtractionFloat
from module_misc.Extractions.ExtractionSource import ExtractionSource
from module_misc.Extractions.Extraction import Extraction
from typing import List
import logging


class Extractor:
    def __init__(self, class_name, name=None):
        self._extractions: List[Extraction] = []
        self._values = {}
        self._single_value = None
        self._single_name = None
        self._single_value_type = None
        self._dominant = None
        self._class_name = class_name
        self._group_name = None
        self._name = name
        self._is_top_level = False
        self._is_exact_single_choice = False

    @property
    def class_name(self):
        return self._class_name

    @property
    def is_single_choice(self):
        return self._is_exact_single_choice

    @property
    def single_value(self):
        return self._single_value

    @property
    def single_name(self):
        return self._single_name

    @property
    def single_value_type(self):
        return self._single_value_type

    def add_str(self, key, specifier=None, valid_values=None, optional=True, default=None, alternative=None,
                description=""):
        extraction = ExtractionStr(key, specifier=specifier, valid_values=valid_values, optional=optional,
                                   default=default, alternative=alternative, description=description)
        self._extractions.append(extraction)

    def add_object(self, key, object_type, specifier=None, optional=True, alternative=None, description=""):
        extraction = ExtractionObject(key, object_type, specifier=specifier, optional=optional,
                                      alternative=alternative, description=description)
        self._extractions.append(extraction)

    def add_bool(self, key, specifier=None, optional=True, default=None, alternative=None, description=""):
        extraction = ExtractionBool(key, specifier=specifier, optional=optional, default=default,
                                    alternative=alternative, description=description)
        self._extractions.append(extraction)

    def add_list(self, key, specifier=None, optional=True, entry_type=None, entry_object_type=None, length=None,
                 min_length=None, valid_values=None, default=None, alternative=None, description=""):
        extraction = ExtractionList(key, specifier=specifier, entry_type=entry_type,
                                    entry_object_type=entry_object_type, length=length, min_length=min_length,
                                    valid_values=valid_values, optional=optional, default=default,
                                    alternative=alternative, description=description)
        self._extractions.append(extraction)

    def add_int(self, key, specifier=None, optional=True, default=None, alternative=None, description=""):
        extraction = ExtractionInt(key, specifier=specifier, optional=optional, default=default,
                                   alternative=alternative, description=description)
        self._extractions.append(extraction)

    def add_float(self, key, specifier=None, optional=True, default=None, alternative=None, description=""):
        extraction = ExtractionFloat(key, specifier=specifier, optional=optional, default=default,
                                     alternative=alternative, description=description)
        self._extractions.append(extraction)

    def add_source(self, key, specifier=None, source_type=None, optional=True, alternative=None, is_dominant=False,
                   description=""):
        extraction = ExtractionSource(key, specifier=specifier, source_type=source_type, optional=optional,
                                      alternative=alternative, is_dominant=is_dominant, description=description)
        self._extractions.append(extraction)

    def get_value(self, key):
        if key in self._values:
            return self._values[key]
        else:
            return None

    def get_extraction(self, key):
        for extraction in self._extractions:
            if extraction.key == key:
                return extraction
        print("KEYERROR:")
        print(key)
        raise KeyError

    @staticmethod
    def key_in_extractions_list(key, extractions_list):
        for extraction in extractions_list:
            if extraction.key == key:
                return True
        return False

    def extraction_has_no_alternative(self, key, extractions):
        has_no_alternative = False
        if key is None:
            has_no_alternative = True
        else:
            if not self.key_in_extractions_list(key, extractions):
                has_no_alternative = True
        return has_no_alternative

    def resolve_alternatives(self):
        sorted_extractions: List[Extraction] = []
        sorted_extractions_keys = []
        remaining_extractions = self._extractions
        last_count_remaining_extractions = len(self._extractions)
        while len(remaining_extractions) > 0:
            next_remaining_extractions: List[Extraction] = []
            for extraction in remaining_extractions:
                has_no_alternative = self.extraction_has_no_alternative(extraction.alternative, remaining_extractions)
                if has_no_alternative:
                    sorted_extractions.insert(0, extraction)
                    sorted_extractions_keys.insert(0, extraction.key)
                else:
                    next_remaining_extractions.append(extraction)
            remaining_extractions = next_remaining_extractions
            if len(remaining_extractions) == last_count_remaining_extractions:
                logging.error("Circular alternatives found.")
                raise ValueError
        self._extractions = sorted_extractions

    def get_dominant_extraction(self):
        for extraction in self._extractions:
            if isinstance(extraction, ExtractionSource):
                if extraction.is_dominant:
                    return extraction
        return None

    def drop_alternatives_recursive(self, key):
        if key is not None:
            extraction = self.get_extraction(key)
            extraction.do_not_extract = True
            if extraction.alternative is not None:
                self.drop_alternatives_recursive(extraction.alternative)

    def drop_alternatives(self, extraction: Extraction):
        if extraction.alternative is not None:
            self.drop_alternatives_recursive(extraction.alternative)

    def use_dominant_extraction(self, parameters):
        dominant_extraction = self.get_dominant_extraction()
        if dominant_extraction is not None:
            extract_value = dominant_extraction.extract(parameters)
            if extract_value is not None:
                self._values.update({
                    dominant_extraction.key: extract_value
                })
                return True
        return False

    @staticmethod
    def check_is_exact_one_value_given(parameters: dict):
        params_keys = list(parameters.keys())
        if "register" in params_keys:
            params_keys.remove("register")
        if "name" in params_keys:
            params_keys.remove("name")
        if len(params_keys) != 1:
            return False
        return True

    def extract_specific_extraction_single_choice(self, parameters):
        if not self.check_is_exact_one_value_given(parameters):
            logging.error("more than one value given")
            raise ValueError
        found = False
        for extraction in self._extractions:
            if not extraction.do_not_extract:
                extract_value = extraction.extract(parameters)
                if extract_value is not None:
                    self.drop_alternatives(extraction)
                if isinstance(extraction, ExtractionObject):
                    if extract_value is not None:
                        self._single_value_type = extraction.object_type
                        self._single_value = extract_value
                        self._single_name = extraction.key
                        found = True
                        break
                else:
                    logging.error("must be an object")
                    raise ValueError
        if not found:
            logging.error("less than one value given. Current values: {}".format(parameters))
            raise ValueError

    def extract_specific_extraction(self, parameters):
        for extraction in self._extractions:
            if not extraction.do_not_extract:
                extract_value = extraction.extract(parameters)
                if extract_value is not None:
                    self.drop_alternatives(extraction)
                value = {
                    extraction.key: extract_value
                }
                self._values.update(value)

    def extract(self, parameters: dict):
        self.resolve_alternatives()
        if self.use_dominant_extraction(parameters):
            return
        if self._is_exact_single_choice:
            self.extract_specific_extraction_single_choice(parameters)
        else:
            self.extract_specific_extraction(parameters)

    def set_main(self):
        self._is_top_level = True

    def set_name(self, name):
        self._name = name

    def set_group_name(self, name):
        self._group_name = name

    def set_exact_single_choice(self):
        self._is_exact_single_choice = True

    def get_structure(self):
        self.resolve_alternatives()
        # dominant_extraction = self.get_dominant_extraction()
        extraction_entries = []
        for extraction in self._extractions:
            extraction_entries.append(extraction.get_structure())
        name = self._name
        if name is None:
            name = self._class_name
        return {
            "class_name": self._class_name,
            "name": name,
            "is_top_level": self._is_top_level,
            "is_single_choice": self._is_exact_single_choice,
            "group_name": self._group_name,
            "arguments": extraction_entries
        }

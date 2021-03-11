import logging
from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent
from module_misc.RegisterData import RegisterCalculationData
import os
from extra_functions import create_directory
import json
import csv


class MetapostInstructionExtractFunctionInfo(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._ids = None
        self._name = None
        self._values_dir = None
        self._value_dicts = {}
        self._entity_type = None
        self._values = None
        self._extractor.add_str("name", optional=False, description="value extractor ID/name")
        valid_entities = ["elem", "node"]
        self._extractor.add_str("entity_type", optional=False, valid_values=valid_entities,
                                description="element_ID or node_ID")
        valid_values = ["max", "min"]
        self._extractor.add_list("values", optional=False, entry_type=str, min_length=1, valid_values=valid_values,
                                 description="value max/min")
        self._variable_names_dict = {
            "max": {"value": "max"},
            "min": {"value": "min"},
        }

    def generate_instruction(self):
        from share_objects import valuesDir
        self._values_dir = os.path.join(valuesDir, self._name)
        create_directory(self._values_dir)
        for slot in self._slots:
            slot_dict = {}
            for fun_val in self._values:
                metapost_variables = self._variable_names_dict[fun_val]
                self.add_command("!function info filter {} on".format(fun_val))
                self.add_slot_command(slot, "function info visible")
                self.add_slot_command(slot, "options var {}identified entity_id".format(self._entity_type))
                fun_vals_dict = {}
                for fun_val_key in metapost_variables.keys():
                    metapost_variable_name = "{}_fun_inf_{}_{}_{}".format(slot, fun_val, self._entity_type, fun_val_key)
                    metapost_variable_filename = "{}.csv".format(metapost_variable_name)
                    output_filename = self.prepare_path_for_metapost_script(
                        os.path.join(self._values_dir, metapost_variable_filename))
                    if self._entity_type == "elem":
                        self.add_slot_command(slot, "options var add {} `ms.sf[eid=$entity_id]`"
                                              .format(metapost_variable_name))
                    if self._entity_type == "node":
                        self.add_slot_command(slot, "options var add {} `ms.sf[nid=$entity_id]`"
                                              .format(metapost_variable_name))
                    self.add_command("options var fileprintlist \"{}\" \"{}\""
                                     .format(metapost_variable_name, output_filename))
                    self.add_command("ide res")
                    fun_vals_dict[fun_val_key] = metapost_variable_filename
                slot_dict[fun_val] = fun_vals_dict
            self._value_dicts[slot] = slot_dict

    def get_arguments(self):
        super().get_arguments()
        self._name = self._extractor.get_value("name")
        self._ids = self._extractor.get_value("ids")
        self._entity_type = self._extractor.get_value("entity_type")
        self._values = self._extractor.get_value("values")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

    def store_values_in_register(self, values_dict):
        from share_objects import register
        if register.get(self._name, None) is not None:
            logging.error("register name already set! Choose a unique name for the data table. Current name: {}"
                          .format(self._name))
            raise ValueError
        register[self._name] = values_dict

    def get_error_variable_missing(self, filename):
        raise NotImplementedError

    def post_metapost_run(self):
        values_dict_output = {}
        for slot in self._slots:
            slot_values_dict = self._value_dicts[slot]
            slot_values_dict_output = {}
            for fun_val in self._values:
                fun_val_values_dict = slot_values_dict[fun_val]
                fun_val_values_dict_output = {}
                for fun_val_key in fun_val_values_dict.keys():
                    value = fun_val_values_dict[fun_val_key]
                    if isinstance(value, str) and value.endswith(".csv"):
                        file_path = os.path.join(self._values_dir, value)
                        with open(file_path, 'r') as csvfile:
                            content = csv.reader(csvfile, delimiter=",")
                            next(content)
                            try:
                                for row in content:
                                    fun_val_values_dict_output[fun_val_key] = float(row[1])
                            except ValueError:
                                self.get_error_variable_missing(value)
                        os.remove(file_path)
                    else:
                        fun_val_values_dict_output[fun_val_key] = value
                slot_values_dict_output[fun_val] = fun_val_values_dict_output
            values_filename = os.path.join(self._values_dir, "values_{}.txt".format(slot))
            with open(values_filename, "w") as f:
                content = json.dumps(slot_values_dict_output)
                f.write(content)
            values_dict_output[slot] = slot_values_dict_output
        values_output = RegisterCalculationData(values=values_dict_output)
        self.store_values_in_register(values_output)

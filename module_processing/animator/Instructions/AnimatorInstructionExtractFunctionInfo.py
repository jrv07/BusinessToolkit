import logging
from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent
from module_misc.RegisterData import RegisterCalculationData
import os
from extra_functions import create_directory
import json


class AnimatorInstructionExtractFunctionInfo(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._ids = None
        self._name = None
        self._values_dir = None
        self._value_dicts = {}
        self._state_mode = None
        self._values = None
        self._extractor.add_str("name", optional=False, description="value extractor ID/name")
        valid_modes = ["global", "current_state"]
        self._extractor.add_str("state_mode", optional=False, valid_values=valid_modes,
                                description="global or current state")
        valid_values = ["max", "min"]
        self._extractor.add_list("values", optional=False, entry_type=str, min_length=1, valid_values=valid_values,
                                 description="value max/min")
        self._variable_names_dict = {
            "max": {"value": "V_MAX", "id": "V_IDMAX", "sta": "V_STAMAX"},
            "min": {"value": "V_MIN", "id": "V_IDMIN", "sta": "V_STAMIN"},
        }

    def generate_instruction(self):
        from share_objects import valuesDir
        self._values_dir = os.path.join(valuesDir, self._name)
        create_directory(self._values_dir)
        data_line_dict = {
            "global": "all",
            "current_state": "act",
        }
        for slot in self._slots:
            slot_dict = {}
            for fun_val in self._values:
                state_mode = data_line_dict[self._state_mode]
                self.add_slot_command(slot, "fun inf {} act {}".format(state_mode, fun_val))
                animator_variables = self._variable_names_dict[fun_val]
                fun_vals_dict = {}
                for fun_val_key in animator_variables.keys():
                    print(fun_val_key)
                    animator_variable_name = "{}_fun_inf_{}_act_{}_{}".format(slot, state_mode, fun_val, fun_val_key)
                    animator_variable_filename = "{}.txt".format(animator_variable_name)
                    output_filename = self.prepare_path_for_animator_script(
                        os.path.join(self._values_dir, animator_variable_filename))
                    # self.add_command("set var num {} {{{}}}".format(animator_variable_name, animator_variables[""]))
                    self.add_command("wri txt {} \"{{{}}}\"".format(output_filename, animator_variables[fun_val_key]))
                    self.add_slot_command(slot, "fun inf {} act {}".format(state_mode, fun_val))
                    fun_vals_dict[fun_val_key] = animator_variable_filename
                slot_dict[fun_val] = fun_vals_dict
            self._value_dicts[slot] = slot_dict
        print(self._value_dicts)

    def get_arguments(self):
        super().get_arguments()
        self._name = self._extractor.get_value("name")
        self._ids = self._extractor.get_value("ids")
        self._state_mode = self._extractor.get_value("state_mode")
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

    def post_animator_run(self):
        values_dict_output = {}
        for slot in self._slots:
            slot_values_dict = self._value_dicts[slot]
            slot_values_dict_output = {}
            for fun_val in self._values:
                fun_val_values_dict = slot_values_dict[fun_val]
                fun_val_values_dict_output = {}
                for fun_val_key in fun_val_values_dict.keys():
                    value = fun_val_values_dict[fun_val_key]
                    if isinstance(value, str) and value.endswith(".txt"):
                        file_path = os.path.join(self._values_dir, value)
                        with open(file_path, 'r') as f:
                            content = f.read()
                            try:
                                if fun_val_key in ["id", "sta"]:
                                    fun_val_values_dict_output[fun_val_key] = int(content)
                                else:
                                    fun_val_values_dict_output[fun_val_key] = float(content)
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
        print(values_dict_output)
        print(values_output)

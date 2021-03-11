import logging
from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent
from module_processing.animator.AnimatorNodeValueExtraction import AnimatorNodeValueExtraction
from module_processing.animator.AnimatorElementValueExtraction import AnimatorElementValueExtraction
import os
from extra_functions import create_directory
import json
from typing import List


class AnimatorInstructionExtractDataAsTable(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._ids = None
        self._name = None
        self._values_dir = None
        self._data_tables = {}
        self._extractor.add_str("name", optional=False, description="Table data extractor ID/name")
        self._extractor.add_list("ids", optional=False, entry_type=int, min_length=1,
                                 description="node_ID or element_ID as list")

    def generate_value_extraction(self, slot, entity_id, function_name):
        raise NotImplementedError

    def generate_instruction(self):
        raise NotImplementedError

    def generate_value_extractions(self):
        raise NotImplementedError

    def get_arguments(self):
        super().get_arguments()
        self._name = self._extractor.get_value("name")
        self._ids = self._extractor.get_value("ids")

    def generate(self):
        super().generate()

    def store_tables_in_register(self, data_tables):
        from share_objects import register
        for slot in self._slots:
            data_table = data_tables[slot]
            register_name = "{}_{}".format(self._name, slot)
            if register.get(register_name, None) is not None:
                logging.error("register name already set! Choose a unique name for the data table. Current name: {}"
                              .format(register_name))
                raise ValueError
            register[register_name] = data_table

    def get_error_id_missing(self, filename):
        raise NotImplementedError

    def post_animator_run(self):
        data_tables_output = {}
        for slot in self._slots:
            data_table_pre = self._data_tables[slot]
            data_table_output = [data_table_pre[0]]
            for line in data_table_pre[1:]:
                output_line = []
                for value in line:
                    if isinstance(value, str) and value.endswith(".txt"):
                        file_path = os.path.join(self._values_dir, value)
                        with open(file_path, 'r') as f:
                            content = f.read()
                            try:
                                output_line.append(float(content))
                            except ValueError:
                                self.get_error_id_missing(value)
                        os.remove(file_path)
                    else:
                        output_line.append(value)
                data_table_output.append(output_line)
            data_tables_output[slot] = data_table_output
            values_filename = os.path.join(self._values_dir, "values_{}.txt".format(slot))
            with open(values_filename, "w") as f:
                content = json.dumps(data_table_output)
                f.write(content)
        self.store_tables_in_register(data_tables_output)


class AnimatorInstructionExtractNodeDataAsTable(AnimatorInstructionExtractDataAsTable):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._value_extractions_input = None
        self._value_extractions: List[AnimatorNodeValueExtraction] = []
        self._variable_names_dict = {
            "x-dis": "V_CU",
            "y-dis": "V_CV",
            "z-dis": "V_CW",
            "total-dis": "V_CT",
            "x-coord-orig": "V_CX",
            "y-coord-orig": "V_CY",
            "z-coord-orig": "V_CZ",
            "x-coord": "V_X",
            "y-coord": "V_Y",
            "z-coord": "V_Z",
        }
        self._extractor.add_list("extractions", optional=False, entry_type=dict,
                                 entry_object_type=AnimatorNodeValueExtraction,
                                 description="choose the data that should be extracted")

    def generate_value_extraction(self, slot, node_id, function_name):
        if function_name == "id":
            return node_id
        animator_function_name = self._variable_names_dict[function_name]
        animator_variable_name = "{}_{}_{}".format(animator_function_name, slot, node_id)
        animator_variable_filename = "{}.txt".format(animator_variable_name)
        output_filename = self.prepare_path_for_animator_script(
            os.path.join(self._values_dir, animator_variable_filename))
        self.add_slot_command(slot, "ide nod {}".format(node_id))
        self.add_slot_command(slot, "set var num {} {{{}}}".format(animator_variable_name, animator_function_name))
        self.add_command("wri txt \"{}\" \"{{V{}}}\"".format(output_filename, animator_variable_name))
        return animator_variable_filename

    def generate_instruction(self):
        from share_objects import valuesDir
        self._values_dir = os.path.join(valuesDir, self._name)
        create_directory(self._values_dir)
        for slot in self._slots:
            first_line = []
            for value_extraction in self._value_extractions:
                first_line.append(value_extraction.label)
            slot_table = [first_line]
            for current_id in self._ids:
                extract_values_of_entity = []
                for value_extraction in self._value_extractions:
                    cell_content = self.generate_value_extraction(slot, current_id, value_extraction.type)
                    extract_values_of_entity.append(cell_content)
                slot_table.append(extract_values_of_entity)
            self._data_tables[slot] = slot_table

    def generate_value_extractions(self):
        if self._value_extractions_input is not None:
            for value_extraction_input in self._value_extractions_input:
                value_extraction = AnimatorNodeValueExtraction(value_extraction_input)
                value_extraction.generate()
                self._value_extractions.append(value_extraction)

    def get_error_id_missing(self, filename):
        node_id = filename.split(".")[0].split("_")[3]
        print("ERROR: node with id {} not contained in model."
              .format(node_id))
        raise ValueError

    def get_arguments(self):
        super().get_arguments()
        self._value_extractions_input = self._extractor.get_value("extractions")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_value_extractions()
            self.generate_instruction()
            self.generate_store_data()


class AnimatorInstructionExtractElementDataAsTable(AnimatorInstructionExtractDataAsTable):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._value_extractions_input = None
        self._value_extractions: List[AnimatorElementValueExtraction] = []
        self._variable_names_dict = {
            "x-dis": "V_CU",
            "y-dis": "V_CV",
            "z-dis": "V_CW",
            "total-dis": "V_CT",
            "part": "V_PI",
            "func": "V_FU",
        }
        self._extractor.add_list("extractions", optional=False, entry_type=dict,
                                 entry_object_type=AnimatorElementValueExtraction,
                                 description="choose extracted data")

    def generate_value_extraction(self, slot, element_id, function_name):
        if function_name == "id":
            return element_id
        data_line_dict = {
            "x-dis": "uel",
            "y-dis": "vel",
            "z-dis": "wel",
            "total-dis": "del"
        }
        output_type = data_line_dict[function_name]
        animator_variable_name = "{}_{}_{}".format(output_type, slot, element_id)
        animator_variable_filename = "{}.txt".format(animator_variable_name)
        output_filename = self.prepare_path_for_animator_script(
            os.path.join(self._values_dir, animator_variable_filename))
        self.add_slot_command(slot, "sty int {} all".format(output_type))
        self.add_slot_command(slot, "ide ele {}".format(element_id))
        self.add_command("set var num {} {{V_FU}}".format(animator_variable_name))
        self.add_command("wri txt {} \"{{V{}}}\"".format(output_filename, animator_variable_name))
        return animator_variable_filename

    def generate_instruction(self):
        from share_objects import valuesDir
        self._values_dir = os.path.join(valuesDir, self._name)
        create_directory(self._values_dir)
        for slot in self._slots:
            first_line = []
            for value_extraction in self._value_extractions:
                first_line.append(value_extraction.label)
            slot_table = [first_line]
            for current_id in self._ids:
                extract_values_of_entity = []
                for value_extraction in self._value_extractions:
                    cell_content = self.generate_value_extraction(slot, current_id, value_extraction.type)
                    extract_values_of_entity.append(cell_content)
                slot_table.append(extract_values_of_entity)
            self._data_tables[slot] = slot_table

    def generate_value_extractions(self):
        if self._value_extractions_input is not None:
            for value_extraction_input in self._value_extractions_input:
                value_extraction = AnimatorElementValueExtraction(value_extraction_input)
                value_extraction.generate()
                self._value_extractions.append(value_extraction)

    def get_error_id_missing(self, filename):
        element_id = filename.split(".")[0].split("_")[2]
        print("ERROR: element with id {} not contained in model."
              .format(element_id))
        raise ValueError

    def get_arguments(self):
        super().get_arguments()
        self._value_extractions_input = self._extractor.get_value("extractions")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_value_extractions()
            self.generate_instruction()
            self.generate_store_data()

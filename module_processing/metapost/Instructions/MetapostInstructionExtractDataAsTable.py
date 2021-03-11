import logging
from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent
from module_processing.metapost.MetapostNodeValueExtraction import MetapostNodeValueExtraction
from module_processing.metapost.MetapostElementValueExtraction import MetapostElementValueExtraction
import os
import csv
from extra_functions import create_directory
import json
from typing import List


class MetapostInstructionExtractDataAsTable(MetapostInstructionSlotDependent):
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

    def post_metapost_run(self):
        data_tables_output = {}
        for slot in self._slots:
            data_table_pre = self._data_tables[slot]
            data_table_output = [data_table_pre[0]]
            for line in data_table_pre[1:]:
                output_line = []
                for value in line:
                    if isinstance(value, str) and value.endswith(".csv"):
                        file_path = os.path.join(self._values_dir, value)
                        with open(file_path, 'r') as csvfile:
                            content = csv.reader(csvfile, delimiter=",")
                            next(content)
                            try:
                                for row in content:
                                    output_line.append(float(row[1]))
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


class MetapostInstructionExtractNodeDataAsTable(MetapostInstructionExtractDataAsTable):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._value_extractions_input = None
        self._value_extractions: List[MetapostNodeValueExtraction] = []
        self._variable_names_dict = {
            "x-dis": "dx",
            "y-dis": "dy",
            "z-dis": "dz",
            "total-dis": "dt",
            "x-coord": "x",
            "y-coord": "y",
            "z-coord": "z",
        }
        self._extractor.add_list("extractions", optional=False, entry_type=dict,
                                 entry_object_type=MetapostNodeValueExtraction,
                                 description="choose the data that should be extracted")

    def generate_value_extraction(self, slot, node_id, function_name):
        if function_name == "id":
            return node_id
        metapost_function_name = self._variable_names_dict[function_name]
        metapost_variable_name = "{}_{}_{}".format(metapost_function_name, slot, node_id)
        metapost_variable_filename = "{}.csv".format(metapost_variable_name)
        output_filename = self.prepare_path_for_metapost_script(
            os.path.join(self._values_dir, metapost_variable_filename))
        self.add_slot_command(slot, "options var add {} `ms.{}[nid={}]`".format(metapost_variable_name,
                                                                                metapost_function_name, node_id))
        self.add_command("options var fileprintlist \"{}\" \"{}\"".format(metapost_variable_name, output_filename))
        return metapost_variable_filename

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
                value_extraction = MetapostNodeValueExtraction(value_extraction_input)
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


class MetapostInstructionExtractElementDataAsTable(MetapostInstructionExtractDataAsTable):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._value_extractions_input = None
        self._value_extractions: List[MetapostElementValueExtraction] = []
        self._variable_names_dict = {
            "x-dis": "c_dx",
            "y-dis": "c_dy",
            "z-dis": "c_dz",
            "total-dis": "c_dtot"
        }
        self._extractor.add_list("extractions", optional=False, entry_type=dict,
                                 entry_object_type=MetapostElementValueExtraction,
                                 description="choose the data that should be extracted")

    def generate_value_extraction(self, slot, element_id, function_name):
        if function_name == "id":
            return element_id
        metapost_function_name = self._variable_names_dict[function_name]
        metapost_variable_name = "{}_{}_{}".format(metapost_function_name, slot, element_id)
        metapost_variable_filename = "{}.csv".format(metapost_variable_name)
        output_filename = self.prepare_path_for_metapost_script(
            os.path.join(self._values_dir, metapost_variable_filename))
        self.add_slot_command(slot, "options var add {} `ms.{}[eid={}]`".format(metapost_variable_name,
                                                                                metapost_function_name, element_id))
        self.add_command("options var fileprintlist  \"{}\" \"{}\"".format(metapost_variable_name, output_filename))
        return metapost_variable_filename

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
                value_extraction = MetapostElementValueExtraction(value_extraction_input)
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

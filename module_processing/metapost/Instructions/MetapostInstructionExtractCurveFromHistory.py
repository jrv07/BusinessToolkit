from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent
from module_misc.RegisterData import RegisterCalculationData
from module_misc.Curves import Curves
from module_misc.Curve import Curve
import os
from extra_functions import create_directory
from pandas import read_csv, isnull
import logging


class MetapostInstructionExtractCurveFromNodeHistory(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._ids = None
        self._name = None
        self._values_dir = None
        self._data_tables = {}
        self._curves = Curves()
        self._value_extractions = []
        self._variable_names_dict = {
            "x-dis": "xdis",
            "y-dis": "ydis",
            "z-dis": "zdis",
            "total-dis": "tdis",
            "x-coord": "xnode",
            "y-coord": "ynode",
            "z-coord": "znode",
        }
        self._extractor.add_str("name", optional=False, description="History data extractor ID/name")
        self._extractor.add_list("ids", optional=False, entry_type=int, min_length=1,
                                 description="node_ID or element_ID")
        valid_extractions = ["x-dis", "y-dis", "z-dis", "total-dis",
                             "x-coord", "y-coord", "z-coord"]
        self._extractor.add_list("extractions", optional=False, entry_type=str, valid_values=valid_extractions,
                                 min_length=1, description="history data type")

    @staticmethod
    def get_history_curve_name(slot, node_id, function_name):
        return "{}_{}_{}".format(function_name, slot, node_id)

    def get_history_curve_filename(self, slot, node_id, function_name):
        metapost_history_name = self.get_history_curve_name(slot, node_id, function_name)
        metapost_history_filename = "{}.csv".format(metapost_history_name)
        return os.path.join(self._values_dir, metapost_history_filename)

    def generate_value_extraction(self, slot, node_id, value_extraction):
        metapost_function_name = self._variable_names_dict[value_extraction]
        file_path = self.get_history_curve_filename(slot, node_id, metapost_function_name)
        file_path_metapost = self.prepare_path_for_metapost_script(file_path)
        window_name = "IdeHistory1"
        curve_id = 1
        self.add_command("xyplot curve delete \"{}\" all".format(window_name))
        self.add_slot_command(slot, "identify history {} {}".format(metapost_function_name, node_id))
        self.add_slot_command(slot, "ide res")
        self.add_command("xyplot options save specialformat column")
        self.add_command("xyplot output file \"{}\" \"{}\" {}".format(window_name, file_path_metapost, curve_id))

    def generate_instruction(self):
        from share_objects import valuesDir
        self._values_dir = os.path.join(valuesDir, self._name)
        create_directory(self._values_dir)
        for slot in self._slots:
            for current_id in self._ids:
                for value_extraction in self._value_extractions:
                    self.generate_value_extraction(slot, current_id, value_extraction)

    def get_arguments(self):
        super().get_arguments()
        self._name = self._extractor.get_value("name")
        self._ids = self._extractor.get_value("ids")
        self._value_extractions = self._extractor.get_value("extractions")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

    def get_error_id_missing(self, filename):
        raise NotImplementedError

    def store_curves_in_register(self):
        from share_objects import register
        if register.get(self._name, None) is not None:
            logging.error("register name already set! Choose a unique name for the data table. Current name: {}"
                          .format(self._name))
            raise ValueError
        register[self._name] = RegisterCalculationData(curves=self._curves)

    def post_metapost_run(self):
        for slot in self._slots:
            for current_id in self._ids:
                for value_extraction in self._value_extractions:
                    file_path = self.get_history_curve_filename(slot, current_id,
                                                                self._variable_names_dict[value_extraction])
                    try:
                        csv_content = read_csv(file_path, sep=",", skip_blank_lines=True, decimal=".", engine='python',
                                               error_bad_lines=True, skiprows=[0, 1, 2, 3, 4], skipfooter=1)
                        number_columns = csv_content.shape[1]
                        if isnull(csv_content.iloc[:, number_columns - 1]).all():
                            csv_content = csv_content.drop(csv_content.columns[[number_columns - 1]], axis=1)
                        curve_title = self.get_history_curve_name(slot, current_id, value_extraction)
                        x_values = csv_content.iloc[:, 0]
                        y_values = csv_content.iloc[:, 1]
                        curve = Curve(curve_title, x_values, y_values)
                        self._curves.add_curve(curve, curve_title)
                    except FileNotFoundError:
                        print("Node Id doesn't exist: {}".format(current_id))
        self.store_curves_in_register()

    def generate_store_data(self):
        self._store_data = RegisterCalculationData(curves=self._curves)


class MetapostInstructionExtractCurveFromHistory(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._name = None
        self._values_dir = None
        self._data_tables = {}
        self._curves = Curves()
        self._value_extractions = []
        self._extractor.add_str("name", optional=False, description="History data extractor ID/name")
        self._extractor.add_list("extractions", optional=False, entry_type=str,
                                 min_length=1, description="history data type")

    @staticmethod
    def get_history_curve_name(slot, extraction_name):
        return "{}_{}".format(extraction_name, slot)

    def get_history_curve_filename(self, slot, extraction_name):
        metapost_history_name = self.get_history_curve_name(slot, extraction_name)
        metapost_history_filename = "{}.csv".format(metapost_history_name)
        return os.path.join(self._values_dir, metapost_history_filename)

    def generate_value_extraction(self, slot, value_extraction):
        metapost_curve_name = value_extraction
        file_path = self.get_history_curve_filename(slot, metapost_curve_name)
        file_path_metapost = self.prepare_path_for_metapost_script(file_path)
        window_name = "Window1"
        self.add_command("xyplot options save specialformat column")
        self.add_command("xyplot output file \"{}\" \"{}\" \"{}\""
                         .format(window_name, file_path_metapost, metapost_curve_name))

    def generate_instruction(self):
        from share_objects import valuesDir
        self._values_dir = os.path.join(valuesDir, self._name)
        create_directory(self._values_dir)
        for slot in self._slots:
            for value_extraction in self._value_extractions:
                self.generate_value_extraction(slot, value_extraction)

    def get_arguments(self):
        super().get_arguments()
        self._name = self._extractor.get_value("name")
        self._value_extractions = self._extractor.get_value("extractions")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

    def get_error_id_missing(self, filename):
        raise NotImplementedError

    def store_curves_in_register(self):
        from share_objects import register
        if register.get(self._name, None) is not None:
            logging.error("register name already set! Choose a unique name for the data table. Current name: {}"
                          .format(self._name))
            raise ValueError
        register[self._name] = RegisterCalculationData(curves=self._curves)

    def post_metapost_run(self):
        for slot in self._slots:
            for value_extraction in self._value_extractions:
                file_path = self.get_history_curve_filename(slot, value_extraction)
                try:
                    csv_content = read_csv(file_path, sep=",", skip_blank_lines=True, decimal=".", engine='python',
                                           error_bad_lines=True, skiprows=[0, 1, 2, 3, 4], skipfooter=1)
                    number_columns = csv_content.shape[1]
                    if isnull(csv_content.iloc[:, number_columns - 1]).all():
                        csv_content = csv_content.drop(csv_content.columns[[number_columns - 1]], axis=1)
                    curve_title = self.get_history_curve_name(slot, value_extraction)
                    x_values = csv_content.iloc[:, 0]
                    y_values = csv_content.iloc[:, 1]
                    curve = Curve(curve_title, x_values, y_values)
                    self._curves.add_curve(curve, curve_title)
                except FileNotFoundError:
                    print("Curve Name doesn't exist: {}".format(value_extraction))
        self.store_curves_in_register()

    def generate_store_data(self):
        self._store_data = RegisterCalculationData(curves=self._curves)

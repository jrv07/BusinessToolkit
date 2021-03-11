import logging
from module_processing.metapost.Instructions.MetapostInstruction import MetapostInstruction


class MetapostInstructionInput(MetapostInstruction):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._input_type = None
        self._file_names = None
        self._displacements = None
        self._functions: list = None
        self._load_all = None
        self._curves = None
        valid_type = ["odb", "inp", "op2", "dat"]
        self._extractor.add_str("type", optional=False, valid_values=valid_type, description="type of input file")
        self._extractor.add_str("filename", optional=False, alternative="filenames", description="file_name")
        self._extractor.add_list("filenames", entry_type=str, optional=False, description="file_name as list")
        self._extractor.add_bool("displacements", optional=False, default=False, description="load displacement on/off")
        self._extractor.add_list("functions", entry_type=str, description="load function_name as list")
        self._extractor.add_bool("curves", optional=False, default=False, description="load curves on/off")

    def add_basic_command(self, file_name):
        if self._input_type == "odb":
            self._commands.append("read geom Abaqus {}".format(file_name))
        elif self._input_type == "inp":
            self._commands.append("read geom Abaqus {}".format(file_name))
        elif self._input_type == "op2":
            self._commands.append("read geom Nastran {}".format(file_name))
        elif self._input_type == "dat":
            self._commands.append("read geom Nastran {}".format(file_name))

    def add_displacements(self, file_name):
        if self._displacements:
            if self._input_type == "odb":
                self._commands.append("read dis Abaqus {} all Displacements".format(file_name))
            elif self._input_type == "op2":
                self._commands.append("read dis Nastran {} all Displacements".format(file_name))

    def add_functions(self, file_name):
        if self._functions is not None:
            for current_function in self._functions:
                if self._input_type == "odb":
                    self.commands.append("function append scalar enable")
                    self.commands.append("read onlyfun Abaqus {} all {}".format(file_name, current_function))
                elif self._input_type == "op2":
                    self.commands.append("function append scalar enable")
                    self.commands.append("read onlyfun Nastran {} all {}".format(file_name, current_function))
            self.commands.remove("function append scalar enable")

    def add_curves(self, file_name):
        window = "Window1"
        if self._curves:
            if self._input_type == "odb":
                self.commands.append("xyplot model load abaqus {}".format(file_name))
                self.commands.append("xyplot create \"{}\"".format(window))
                self.commands.append("xyplot read Abaqus \"{}\" \"{}\" Nodal all \"all\" \"all\""
                                     .format(window, file_name))
            elif self._input_type == "op2":
                self.commands.append("xyplot model load nastran {}".format(file_name))
                self.commands.append("xyplot create \"{}\"".format(window))
                self.commands.append("xyplot read op2 \"{}\" \"{}\" loadstep displacements all all \"all\" all"
                                     .format(window, file_name))
                self.commands.append("xyplot read op2 \"{}\" \"{}\" loadstep appliedloads all all \"all\" all"
                                     .format(window, file_name))

    def generate_instruction_load_odb(self, file_name):
        self.add_basic_command(file_name)
        self.add_displacements(file_name)
        self.add_functions(file_name)
        self.add_curves(file_name)

    def generate_instruction_load_op2(self, file_name):
        self.add_basic_command(file_name)
        self.add_displacements(file_name)
        self.add_functions(file_name)
        self.add_curves(file_name)

    def generate_instruction_load_inp(self, file_name):
        self.add_basic_command(file_name)

    def generate_instruction_load_dat(self, file_name):
        self.add_basic_command(file_name)

    def generate_instruction(self):
        for current_filename in self._file_names:
            if self._input_type == "odb":
                self.generate_instruction_load_odb(current_filename)
            elif self._input_type == "inp":
                self.generate_instruction_load_inp(current_filename)
            elif self._input_type == "op2":
                self.generate_instruction_load_op2(current_filename)
            elif self._input_type == "dat":
                self.generate_instruction_load_dat(current_filename)
            logging.info('load {}: using command:\n{}'.format(self._input_type, self._commands))

    def get_arguments(self):
        self._input_type = self._extractor.get_value("type")
        self.get_file_names()
        self._displacements = self._extractor.get_value("displacements")
        self._functions = self._extractor.get_value("functions")
        self._curves = self._extractor.get_value("curves")

    def get_file_names(self):
        file_name = self._extractor.get_value("filename")
        if file_name is None:
            self._file_names = self._extractor.get_value("filenames")
        else:
            self._file_names = [file_name]

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

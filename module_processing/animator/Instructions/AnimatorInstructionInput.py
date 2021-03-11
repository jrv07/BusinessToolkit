import logging
from module_processing.animator.Instructions.AnimatorInstruction import AnimatorInstruction


class AnimatorInstructionInput(AnimatorInstruction):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._input_type = None
        self._file_names = None
        self._displacements = None
        self._modal = None
        self._functions: list = None
        self._load_all = None
        self._curves = None
        valid_type = ["a3db", "a4db", "odb", "inp", "op2", "dat"]
        self._extractor.add_str("type", optional=False, valid_values=valid_type, description="type of input file")
        self._extractor.add_str("filename", optional=False, alternative="filenames", description="file_name")
        self._extractor.add_list("filenames", entry_type=str, optional=False, description="file_name as list")
        self._extractor.add_bool("displacements", optional=False, default=False, description="load displacement on/off")
        self._extractor.add_bool("modal", optional=False, default=False, description="load modal on/off")
        self._extractor.add_list("curves", entry_type=str, description="load curves on/off")
        self._extractor.add_bool("load_all", optional=False, default=False, description="load everything")
        self._extractor.add_list("functions", entry_type=str, description="load function_name as list")

    def add_basic_command(self, command_parts, file_name):
        if self._input_type == "a3db":
            command_parts.append('s[new]:rea fil Database "{}" GEO=0:pid:all'.format(file_name))
        elif self._input_type == "odb":
            command_parts.append("s[new]:rea fil 'Abaqus_auto' '{}' GEO=0:pid:all".format(file_name))
        elif self._input_type == "inp":
            command_parts.append("s[new]:rea fil 'Abaqus_auto' '{}' GEO=0:pid:all".format(file_name))
        elif self._input_type == "op2":
            command_parts.append('s[new]:rea fil "Nastran" "{}" GEO=0:pid:all'.format(file_name))
        elif self._input_type == "dat":
            command_parts.append('s[new]:rea fil "Nastran" "{}" GEO=0:pid:all'.format(file_name))
        elif self._input_type == "a4db":
            command_parts.append('rea da4 "{}"'.format(file_name))

    def add_displacements(self, command_parts):
        if self._displacements:
            if self._input_type == "a3db":
                command_parts.append('DIS=0:all')
            elif self._input_type == "odb":
                command_parts.append('DIS=0:all')
            elif self._input_type == "inp":
                command_parts.append('DIS=0:all')
            elif self._input_type == "op2":
                command_parts.append('DIS=0:all')
            elif self._input_type == "dat":
                command_parts.append('DIS=0:all')
            elif self._input_type == "a4db":
                command_parts.append('DIS=0:"Set 0":all')

    def add_functions(self, command_parts):
        if self._functions is not None:
            if len(self._functions) > 0:
                for current_function in self._functions:
                    if self._input_type == "a3db":
                        command_parts.append('FUN=0:all:"{}"'.format(current_function))
                    elif self._input_type == "odb":
                        command_parts.append('FUN=0:all:"{}"'.format(current_function))
                    elif self._input_type == "op2":
                        command_parts.append('FUN=0:all:"{}"'.format(current_function))
                    elif self._input_type == "a4db":
                        command_parts.append('FUN=0:"Set 0":"{}":all'.format(current_function))

    def add_curves(self, command_parts):
        if self._curves is not None:
            command_parts_curves = map(lambda curve_str: '"{}"'.format(curve_str), self._curves)
            command_curves = "/".join(command_parts_curves)
            command_parts.append("C2D=0:{}".format(command_curves))
        else:
            command_parts.append("C2D=0:all")

    def add_misc(self, command_parts):
        # Todo: what is necessary? Or in basic command?
        if self._input_type == "a3db":
            command_parts.append('ADD=no')
        elif self._input_type == "odb":
            command_parts.append('ADD=no')
        elif self._input_type == "inp":
            command_parts.append('ADD=no')
        elif self._input_type == "op2":
            command_parts.append('ADD=no')
        elif self._input_type == "dat":
            command_parts.append('ADD=no')
        elif self._input_type == "a4db":
            command_parts.append("GEO=0:all")
            command_parts.append("IMG=all")
            command_parts.append("VID=all")
            command_parts.append("VAR=all")
            command_parts.append("SET=all")
            command_parts.append('ADD=yes')

    def generate_instruction_load_a3db(self, command_parts, file_name):
        self.add_basic_command(command_parts, file_name)
        self.add_displacements(command_parts)
        self.add_functions(command_parts)
        self.add_misc(command_parts)

    def generate_instruction_load_odb(self, command_parts, file_name):
        self.add_basic_command(command_parts, file_name)
        self.add_displacements(command_parts)
        self.add_functions(command_parts)
        self.add_misc(command_parts)

    def generate_instruction_load_inp(self, command_parts, file_name):
        self.add_basic_command(command_parts, file_name)
        self.add_displacements(command_parts)
        self.add_misc(command_parts)

    def generate_instruction_load_op2(self, command_parts, file_name):
        self.add_basic_command(command_parts, file_name)
        self.add_displacements(command_parts)
        self.add_functions(command_parts)
        self.add_misc(command_parts)

    def generate_instruction_load_dat(self, command_parts, file_name):
        self.add_basic_command(command_parts, file_name)
        self.add_displacements(command_parts)
        self.add_misc(command_parts)

    def generate_instruction_load_a4db(self, command_parts, file_name):
        self.add_basic_command(command_parts, file_name)
        if not self._load_all:
            self.add_curves(command_parts)
            self.add_displacements(command_parts)
            self.add_functions(command_parts)
            self.add_misc(command_parts)

    def generate_instruction(self):
        if self._modal is True:
            self.add_command('opt ana mod on')
        for current_filename in self._file_names:
            command_parts = []
            if self._input_type == "a3db":
                self.generate_instruction_load_a3db(command_parts, current_filename)
            elif self._input_type == "odb":
                self.generate_instruction_load_odb(command_parts, current_filename)
            elif self._input_type == "inp":
                self.generate_instruction_load_inp(command_parts, current_filename)
            elif self._input_type == "op2":
                self.generate_instruction_load_op2(command_parts, current_filename)
            elif self._input_type == "dat":
                self.generate_instruction_load_dat(command_parts, current_filename)
            elif self._input_type == "a4db":
                self.generate_instruction_load_a4db(command_parts, current_filename)

            self._commands.append(" ".join(command_parts))
            logging.info('load {}: using command:\n{}'.format(self._input_type, self._commands))

    def get_arguments(self):
        self._input_type = self._extractor.get_value("type")
        self.generate_file_names()
        self._displacements = self._extractor.get_value("displacements")
        self._modal = self._extractor.get_value("modal")
        self._curves = self._extractor.get_value("curves")
        self._load_all = self._extractor.get_value("load_all")
        self._functions = self._extractor.get_value("functions")

    def generate_file_names(self):
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

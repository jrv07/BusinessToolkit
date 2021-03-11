from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent
from module_misc.RegisterData import RegisterPostProcessorWriteInstructionData
import os
import logging


class MetapostInstructionWrite(MetapostInstructionSlotDependent):
    def __init__(self, parameters, directory, valid_formats):
        super().__init__(parameters)
        self._file_name = None
        self._file_path = None
        self._file_path_in_script = None
        self._format = None
        self._directory = directory
        self._valid_formats = valid_formats
        self._extractor.add_str("filename", optional=False, description="output file name")
        self._extractor.add_str("format", valid_values=valid_formats, description="output file format")

    @property
    def file_path(self):
        return self._file_path

    def generate_file_name_and_format(self):
        file_name = self._file_name
        format_value = self._format
        base_name, extension = os.path.splitext(file_name)
        if extension != "":
            extension = extension[1:].lower()
            if extension not in self._valid_formats:
                logging.error("Invalid extension: {}"
                              .format(file_name))
                raise ValueError
            if format_value is not None:
                if extension != format_value:
                    logging.error("Extension {} and format {} not matching.".format(file_name, format_value)
                                  .format(file_name))
                    raise ValueError
        else:
            if format_value is not None:
                extension = format_value
                self._format = extension.lower()
            else:
                logging.error("Invalid Filename: {}"
                              .format(file_name))
                raise ValueError

        self._file_name = "{}.{}".format(base_name, extension)

    def generate_file_path(self):
        self._file_path = os.path.join(self._directory, self._file_name)
        self._file_path_in_script = self.prepare_path_for_metapost_script(self._file_path)

    def generate_instruction(self):
        raise NotImplementedError

    def get_arguments(self):
        super().get_arguments()
        self._file_name = self._extractor.get_value("filename")
        self._format = self._extractor.get_value("format")

    def generate_store_data(self):
        self._store_data = RegisterPostProcessorWriteInstructionData(self._commands, self._file_path)

    def generate(self):
        super().generate()


class MetapostInstructionWritePicture(MetapostInstructionWrite):
    def __init__(self, parameters):
        from share_objects import picturesDir
        valid_formats = ["jpeg", "png"]
        super().__init__(parameters, picturesDir, valid_formats)

    def generate_instruction(self):
        for slot in self._slots:
            self.add_slot_command(slot, "write {} {}".format(self._format, self._file_path_in_script))

    def get_arguments(self):
        super().get_arguments()

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_file_name_and_format()
            self.generate_file_path()
            self.generate_instruction()
            self.generate_store_data()


class MetapostInstructionWriteMovie(MetapostInstructionWrite):
    def __init__(self, parameters):
        from share_objects import moviesDir
        valid_formats = ["gif", "avi"]
        super().__init__(parameters, moviesDir, valid_formats)
        self._state_range = None
        self._speed = None
        self._animation = None
        self._extractor.add_list("state_range", entry_type=int, length=2, description="")
        self._extractor.add_int("speed", description="")
        self._extractor.add_str("animation", valid_values=["forward", "backward", "fab"],
                                optional=False, default="fo1", description="")

    def generate_instruction(self):
        for slot in self._slots:
            if self._state_range is not None:
                vec = list(map(lambda vec_entry: str(vec_entry), self._state_range))
                self.add_slot_command(slot, "options state animation range set {}".format(" ".join(vec)))
            if self._speed is not None:
                self.add_slot_command(slot, "record {} fps {}".format(self._format, str(self._speed)))
            self.add_slot_command(slot, "record movie {} loop 1 {} {}"
                                  .format(self._animation, self._format, self._file_path))

    def get_arguments(self):
        super().get_arguments()
        self._state_range = self._extractor.get_value("state_range")
        self._speed = self._extractor.get_value("speed")
        self._animation = self._extractor.get_value("animation")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_file_name_and_format()
            self.generate_file_path()
            self.generate_instruction()
            self.generate_store_data()

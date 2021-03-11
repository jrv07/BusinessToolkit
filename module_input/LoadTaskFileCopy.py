from module_input.LoadTaskFile import LoadTaskFile
from module_misc.RegisterData import RegisterFile
from shutil import copyfile
import logging
import os


class LoadTaskFileCopy(LoadTaskFile):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._import_file_path = None

    @property
    def import_file_path(self):
        return self._import_file_path

    def load_from_file(self):
        try:
            copyfile(self._file_path, self._import_file_path)
        except FileNotFoundError:
            logging.error("File {} does not exist".format(self._file_path))
            raise FileNotFoundError
        except Exception as exception:
            logging.error(exception)
            raise ValueError

    def generate_import_file_path(self, import_directory):
        basename = os.path.basename(self._file_path)
        self._import_file_path = os.path.join(import_directory, basename)

    def generate_import_file(self, import_directory):
        self.generate_import_file_path(import_directory)
        self.load_from_file()
        self.generate_store_data()

    def generate_store_data(self):
        self._store_data = RegisterFile(self._import_file_path)

    def generate(self):
        super().generate()

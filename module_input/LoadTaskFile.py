from module_misc.WithStoreData import WithStoreData


class LoadTaskFile(WithStoreData):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._file_path = None
        self._extractor.add_str("file_path", optional=False)
        self._extractor.set_group_name("ReadData")

    def generate_store_data(self):
        raise NotImplementedError

    def get_arguments(self):
        super().get_arguments()
        self._file_path = self._extractor.get_value("file_path")

    def generate(self):
        super().generate()

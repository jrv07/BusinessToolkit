from module_misc.BasicTask import BasicTask


class MetapostSettings(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._version = None
        self._options = None
        self._script_type = None
        self._extractor.add_str("version", optional=False, description="")
        self._extractor.add_str("options", optional=False, default="", description="")
        self._extractor.add_str("script_type", valid_values=["python", "session"], optional=False, description="")
        self._extractor.set_group_name("Processing.Metapost")

    @property
    def script_type(self):
        return self._script_type

    @property
    def version(self):
        return self._version

    @property
    def options(self):
        return self._options

    def get_arguments(self):
        super().get_arguments()
        self._version = self._extractor.get_value("version")
        self._options = self._extractor.get_value("options")
        self._script_type = self._extractor.get_value("script_type")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()

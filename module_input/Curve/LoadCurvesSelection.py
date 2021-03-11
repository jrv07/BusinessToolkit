from module_misc.BasicTask import BasicTask


class LoadCurvesSelection(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._register = None
        self._extractor.add_str("register", description="")
        self._extractor.set_group_name("ReadData")

    @property
    def register(self):
        return self._register

    def get_arguments(self):
        self._register = self._extractor.get_value("register")

    def generate(self):
        super().generate()

from module_misc.BasicTask import BasicTask


class AnimatorNodeValueExtraction(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._type = None
        self._label = None
        self._valid_extractions = ["id", "x-dis", "y-dis", "z-dis", "total-dis", "x-coord-orig", "y-coord-orig",
                                   "z-coord-orig", "x-coord", "y-coord", "z-coord", "usr_var"]
        self._extractor.add_str("type", optional=False, valid_values=self._valid_extractions,
                                description="type of value extraction")
        self._extractor.add_str("label", optional=False, description="label for extracted values")
        self._extractor.set_group_name("Processing.Animator")

    @property
    def type(self):
        return self._type

    @property
    def label(self):
        return self._label

    def get_arguments(self):
        self._type = self._extractor.get_value("type")
        self._label = self._extractor.get_value("label")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()

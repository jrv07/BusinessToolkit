from module_input.Curve.LoadCurvesSelection import LoadCurvesSelection


class LoadCurvesSelectionBinout(LoadCurvesSelection):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._curve_path = None
        self._function_names = None
        self._ids = None
        self._name = None
        self._extractor.add_list("curve_path", entry_type=str, optional=False, description="")
        self._extractor.add_list("ids", entry_type=str, description="")
        self._extractor.add_list("name", entry_type=str, description="")
        self._extractor.add_list("function_names", entry_type=str, optional=False)

    @property
    def curve_path(self):
        return self._curve_path

    @property
    def requested_ids(self):
        return self._ids

    @property
    def requested_name(self):
        return self._name

    @property
    def function_names(self):
        return self._function_names

    def get_arguments(self):
        super().get_arguments()
        self._curve_path = self._extractor.get_value("curve_path")
        self._ids = self._extractor.get_value("ids")
        self._name = self._extractor.get_value("name")
        self._function_names = self._extractor.get_value("function_names")

    def generate(self):
        self.extract()
        self.get_arguments()

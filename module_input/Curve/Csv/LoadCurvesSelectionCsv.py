from module_input.Curve.LoadCurvesSelection import LoadCurvesSelection


class LoadCurvesSelectionCsv(LoadCurvesSelection):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._curve_title = None
        self._extractor.add_str("curve_title", optional=False, description="")

    @property
    def curve_title(self):
        return self._curve_title

    def get_arguments(self):
        super().get_arguments()
        self._extractor.get_value("curve_title")

    def generate(self):
        self.extract()
        self.get_arguments()

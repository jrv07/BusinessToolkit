from module_misc.BasicTask import BasicTask
from module_misc.RegisterData import RegisterCalculationData


class CurveSelection(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._curve_data_source: RegisterCalculationData = None
        self._tag = None
        self._extractor.add_source("curve_data_source", source_type=RegisterCalculationData, optional=False, description="")
        self._extractor.add_str("tag", optional=False, description="")
        self._extractor.set_group_name("Processing.Arrk")

    @property
    def curve(self):
        return self._curve_data_source.curves.get_curve(self._tag)

    def get_arguments(self):
        super().get_arguments()
        self._tag = self._extractor.get_value("tag")
        self._curve_data_source = self._extractor.get_value("curve_data_source")

    def generate(self):
        self.extract()
        self.get_arguments()

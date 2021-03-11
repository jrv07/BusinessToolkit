from module_misc.BasicTask import BasicTask
from module_misc.Curves import Curves


class CurveCalculatorCurveOutput(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._curve_name = None
        self._tag = None
        self._extractor.add_str("curve", optional=False, description="")
        self._extractor.add_str("tag", optional=False, description="")
        self._extractor.set_group_name("Processing.Arrk")

    def apply(self, curves: Curves, output: Curves):
        curve = curves.get_curve(self._curve_name)
        output.add_curve(curve, self._tag)

    def get_arguments(self):
        super().get_arguments()
        self._curve_name = self._extractor.get_value("curve")
        self._tag = self._extractor.get_value("tag")

    def generate(self):
        self.extract()
        self.get_arguments()

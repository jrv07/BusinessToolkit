from module_misc.Curve import Curve
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstruction import CurveCalculationInstruction
from module_misc.Curves import Curves


class CurveCalculationInstructionScaleY(CurveCalculationInstruction):
    def __init__(self, parameters):
        super().__init__(parameters, "potentiation", in_min_length_required=1, out_equals_in_length=True)
        self._factor = None
        self._extractor.add_float("factor", optional=False, default=1, description="")

    def apply_modification(self, curve: Curve) -> Curve:
        return Curve(curve.name, curve.df.X, curve.df.Y * self._factor)

    def calculate(self, curves: Curves, values: dict):
        for curve_index, curve_name in enumerate(self._curve_names):
            curve_scale = curves.get_curve(curve_name)
            curve_scale = self.apply_modification(curve_scale)
            curves.add_curve(curve_scale, self._result_curves[curve_index])

    def get_arguments(self):
        super().get_arguments()
        self._factor = self._extractor.get_value("factor")

    def generate(self):
        self.extract()
        self.get_arguments()

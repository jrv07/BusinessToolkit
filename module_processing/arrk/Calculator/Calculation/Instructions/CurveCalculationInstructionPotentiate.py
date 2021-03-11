from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstruction import CurveCalculationInstruction
from module_misc.Curves import Curves


class CurveCalculationInstructionPotentiate(CurveCalculationInstruction):
    def __init__(self, parameters):
        super().__init__(parameters, "potentiation", in_min_length_required=1, out_equals_in_length=True)
        self._power = None
        self._extractor.add_float("power", optional=False, description="")

    def calculate(self, curves: Curves, values: dict):
        for curve_index, curve_name in enumerate(self._curve_names):
            curve_power = curves.get_curve(curve_name)
            curve_power = curve_power ** self._power
            curves.add_curve(curve_power, self._result_curves[curve_index])

    def get_arguments(self):
        super().get_arguments()
        self._power = self._extractor.get_value("power")

    def generate(self):
        self.extract()
        self.get_arguments()

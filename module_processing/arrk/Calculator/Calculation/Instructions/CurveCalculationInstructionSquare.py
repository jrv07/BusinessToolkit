from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstruction import CurveCalculationInstruction
from module_misc.Curves import Curves


class CurveCalculationInstructionSquare(CurveCalculationInstruction):
    def __init__(self, parameters):
        super().__init__(parameters, "square", in_min_length_required=1, out_equals_in_length=True)

    def calculate(self, curves: Curves, values: dict):
        for curve_index, curve_name in enumerate(self._curve_names):
            curve_power = curves.get_curve(curve_name)
            curve_power = curve_power ** 2
            curves.add_curve(curve_power, self._result_curves[curve_index])

    def generate(self):
        self.extract()
        self.get_arguments()

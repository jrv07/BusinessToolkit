from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstruction import CurveCalculationInstruction
from module_misc.Curves import Curves


class CurveCalculationInstructionDivide(CurveCalculationInstruction):
    def __init__(self, parameters):
        super().__init__(parameters, "division", in_length_required=2, out_length_required=1)

    def calculate(self, curves: Curves, values: dict):
        curve_quotient = curves.get_curve(self._curve_names[0])
        curve_quotient = curve_quotient / curves.get_curve(self._curve_names[1])
        curves.add_curve(curve_quotient, self._result_curves[0])

    def generate(self):
        self.extract()
        self.get_arguments()

from module_processing.arrk.Calculator.Calculation.Instructions.ValueCalculationInstruction \
    import ValueCalculationInstruction
from module_misc.Curves import Curves


class ValueCalculationInstructionMax(ValueCalculationInstruction):
    def __init__(self, parameters):
        super().__init__(parameters, "max", in_min_length_required=1)

    def calculate(self, curves: Curves, values: dict):
        total_max = None
        for curve_name in self._curve_names:
            current_curve = curves.get_curve(curve_name)
            current_max = current_curve.max()
            if total_max is None:
                total_max = current_max
            else:
                if current_max > total_max:
                    total_max = current_max
        values[self._result_value_name] = total_max

    def generate(self):
        self.extract()
        self.get_arguments()

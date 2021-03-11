from module_processing.arrk.Calculator.Calculation.Instructions.ValueCalculationInstruction \
    import ValueCalculationInstruction
from module_misc.Curves import Curves


class ValueCalculationInstructionMin(ValueCalculationInstruction):
    def __init__(self, parameters):
        super().__init__(parameters, "min", in_min_length_required=1)

    def calculate(self, curves: Curves, values: dict):
        total_min = None
        for curve_name in self._curve_names:
            current_curve = curves.get_curve(curve_name)
            current_min = current_curve.min()
            if total_min is None:
                total_min = current_min
            else:
                if current_min < total_min:
                    total_min = current_min
        values[self._result_value_name] = total_min

    def generate(self):
        self.extract()
        self.get_arguments()

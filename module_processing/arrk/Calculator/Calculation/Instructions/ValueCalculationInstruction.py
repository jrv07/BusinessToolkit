from module_processing.arrk.Calculator.Calculation.Instructions.CalculationInstruction import CalculationInstruction
from module_misc.Curves import Curves


class ValueCalculationInstruction(CalculationInstruction):
    def __init__(self, parameters, instruction_name, in_length_required=None, in_min_length_required=None):
        super().__init__(parameters, instruction_name=instruction_name, in_length_required=in_length_required,
                         in_min_length_required=in_min_length_required)
        self._result_value_name = None
        self._extractor.add_str("result_value_name", optional=False, description="")

    @property
    def name(self):
        return self._result_value_name

    def calculate(self, curves: Curves, values: dict):
        raise NotImplementedError

    def get_result(self):
        self._result_value_name = self._extractor.get_value("result_value_name")

    def get_arguments(self):
        super().get_arguments()
        self.get_result()

    def generate(self):
        pass

from module_processing.arrk.Calculator.Calculation.Instructions.CalculationInstruction import CalculationInstruction
from module_misc.Curves import Curves
import logging


class CurveCalculationInstruction(CalculationInstruction):
    def __init__(self, parameters, instruction_name, in_length_required=None, in_min_length_required=None,
                 out_equals_in_length=False, out_length_required=None):
        super().__init__(parameters, instruction_name=instruction_name, in_length_required=in_length_required,
                         in_min_length_required=in_min_length_required)
        self._out_equals_in_length = out_equals_in_length
        self._out_length_required = out_length_required
        self._result_curves = None
        self._extractor.add_str("result_curve", optional=False, alternative="result_curves", description="")
        self._extractor.add_list("result_curves", entry_type=str, optional=False, description="")

    @property
    def names(self):
        return self._result_curves

    def calculate(self, curves: Curves, values: dict):
        raise NotImplementedError

    def get_result(self):
        out_name = self._extractor.get_value("result_curve")
        if out_name is not None:
            self._result_curves = [out_name]
        else:
            self._result_curves = self._extractor.get_value("result_curves")

        if self._out_equals_in_length:
            if len(self._curve_names) != len(self._result_curves):
                logging.error("specification of the same amount of output curve names as input curves is "
                              "required. Instruction: {}, Current values: {}"
                              .format(self._instruction_name, self._curve_names))
                raise ValueError
        else:
            if self._out_length_required is not None:
                if self._out_length_required != len(self._result_curves):
                    logging.error("specification of exactly {} output curve names is required. "
                                  "Instruction: {}, Current values: {}"
                                  .format(self._out_length_required, self._instruction_name, self._curve_names))
                    raise ValueError

    def get_arguments(self):
        super().get_arguments()
        self.get_result()

    def generate(self):
        pass

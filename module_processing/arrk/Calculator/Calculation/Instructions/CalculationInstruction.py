from module_misc.BasicTask import BasicTask
from module_misc.Curves import Curves


class CalculationInstruction(BasicTask):
    def __init__(self, parameters, instruction_name, in_length_required=None, in_min_length_required=None):
        super().__init__(parameters)
        self._in_min_length_required = in_min_length_required
        self._in_length_required = in_length_required
        self._instruction_name = instruction_name
        self._curve_names = None
        self._extractor.add_str("curve", optional=False, alternative="curves", description="")
        self._extractor.add_list("curves", entry_type=str, length=self._in_length_required,
                                 min_length=self._in_min_length_required, optional=False, description="")
        self._extractor.set_group_name("Processing.Arrk")

    @property
    def curve_names(self):
        return self._curve_names

    def calculate(self, curves: Curves, values: dict):
        raise NotImplementedError

    def get_curve_names(self):
        curve_name = self._extractor.get_value("curve")
        if curve_name is None:
            self._curve_names = self._extractor.get_value("curves")
        else:
            self._curve_names = [curve_name]

    def get_result(self):
        raise NotImplementedError

    def get_arguments(self):
        super().get_arguments()
        self.get_curve_names()

    def generate(self):
        pass

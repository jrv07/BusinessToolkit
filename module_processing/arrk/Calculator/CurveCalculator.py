from module_misc.WithStoreData import WithStoreData
from module_processing.arrk.Calculator.CurveCalculatorCurveOutput import CurveCalculatorCurveOutput
from module_processing.arrk.Calculator.Calculation.CurveCalculation import CurveCalculation
from module_processing.arrk.Calculator.CurveCalculatorInput import CurveCalculatorInput
from module_misc.RegisterData import RegisterCalculationData
from module_misc.Curves import Curves


class CurveCalculator(WithStoreData):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._curve_inputs_input = None
        self._curve_outputs_input = None
        self._calculation_input = None
        self._extractor.add_list("inputs", entry_type=dict, entry_object_type=CurveCalculatorInput, optional=False,
                                 description="")
        self._extractor.add_list("curve_outputs", entry_type=dict, entry_object_type=CurveCalculatorCurveOutput,
                                 optional=False, description="")
        self._extractor.add_object("calculation", object_type=CurveCalculation, optional=False)
        self._extractor.set_group_name("Processing.Arrk")
        self._curve_inputs: Curves = Curves()
        self._curve_outputs: Curves = Curves()
        self._values = {}
        self._calculation: CurveCalculation = None

    def generate_inputs(self):
        for selection_input in self._curve_inputs_input:
            selection = CurveCalculatorInput(selection_input)
            selection.generate()
            self._curve_inputs.add_curve(selection.curve, selection.name)

    def generate_calculation(self):
        calculation = CurveCalculation(self._calculation_input)
        calculation.generate()
        self._calculation = calculation

    def calculate(self):
        self._calculation.calculate(self._curve_inputs, self._values)

    def generate_outputs(self):
        for curve_output_input in self._curve_outputs_input:
            curve_output = CurveCalculatorCurveOutput(curve_output_input)
            curve_output.generate()
            curve_output.apply(self._curve_inputs, self._curve_outputs)

    def generate_store_data(self):
        self._store_data = RegisterCalculationData(curves=self._curve_outputs, values=self._values)
        print(self._values)

    def get_arguments(self):
        super().get_arguments()
        self._curve_inputs_input = self._extractor.get_value("inputs")
        self._curve_outputs_input = self._extractor.get_value("curve_outputs")
        self._calculation_input = self._extractor.get_value("calculation")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_inputs()
        self.generate_calculation()
        self.calculate()
        self.generate_outputs()
        self.generate_store_data()
        self.store_in_register()

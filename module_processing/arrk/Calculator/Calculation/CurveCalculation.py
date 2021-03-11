from module_misc.BasicTask import BasicTask
from module_processing.arrk.Calculator.Calculation.CurveCalculationInstructionFactory import \
    CurveCalculationInstructionFactory
from module_processing.arrk.Calculator.Calculation.Instructions.CalculationInstruction import CalculationInstruction
from module_misc.Curves import Curves
from typing import List
import logging


class CurveCalculation(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._instructions_input = None
        self._expression = None
        self._extractor.add_list("instructions", entry_type=dict, entry_object_type=CurveCalculationInstructionFactory,
                                 description="")
        self._extractor.add_str("expression", description="")
        self._extractor.set_group_name("Processing.Arrk")
        self._instructions: List[CalculationInstruction] = []

    def validate_input(self):
        if self._instructions_input is None and self._expression is None:
            logging.error("Either \"instructions\" or \"expression\" for calculation needed")
            raise ValueError
        if self._instructions_input is not None and self._expression is not None:
            logging.error("Only one of \"instructions\" or \"expression\" may be given.")
            raise ValueError

    def generate_instructions(self):
        for instruction_input in self._instructions_input:
            instruction_factory = CurveCalculationInstructionFactory(instruction_input)
            instruction_factory.generate()
            self._instructions.append(instruction_factory.instruction)

    def calculate(self, curves: Curves, values: dict):
        for instruction in self._instructions:
            instruction.calculate(curves, values)

    def get_arguments(self):
        super().get_arguments()
        self._instructions_input = self._extractor.get_value("instructions")
        self._expression = self._extractor.get_value("expression")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.validate_input()
        self.generate_instructions()

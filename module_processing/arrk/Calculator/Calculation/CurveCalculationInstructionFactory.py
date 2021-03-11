from module_misc.InstructionFactory import InstructionFactory
from module_processing.arrk.Calculator.Calculation.Instructions.CalculationInstruction import \
    CalculationInstruction
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionAdd import \
    CurveCalculationInstructionAdd
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionSubtract import \
    CurveCalculationInstructionSubtract
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionMultiply import \
    CurveCalculationInstructionMultiply
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionDivide import \
    CurveCalculationInstructionDivide
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionPotentiate import \
    CurveCalculationInstructionPotentiate
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionSquare import \
    CurveCalculationInstructionSquare
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionSquareRoot import \
    CurveCalculationInstructionSquareRoot
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionLog import \
    CurveCalculationInstructionLog
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionExp import \
    CurveCalculationInstructionExp
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionFilter import \
    CurveCalculationInstructionFilter
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionScaleX import \
    CurveCalculationInstructionScaleX
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionScaleY import \
    CurveCalculationInstructionScaleY
from module_processing.arrk.Calculator.Calculation.Instructions.ValueCalculationInstructionMin import \
    ValueCalculationInstructionMin
from module_processing.arrk.Calculator.Calculation.Instructions.ValueCalculationInstructionMax import \
    ValueCalculationInstructionMax


class CurveCalculationInstructionFactory(InstructionFactory):
    def __init__(self, parameters):
        super().__init__(parameters, CalculationInstruction)
        self._extractor.add_object("add", CurveCalculationInstructionAdd, description="")
        self._extractor.add_object("subtract", CurveCalculationInstructionSubtract, description="")
        self._extractor.add_object("multiply", CurveCalculationInstructionMultiply, description="")
        self._extractor.add_object("divide", CurveCalculationInstructionDivide, description="")
        self._extractor.add_object("potentiate", CurveCalculationInstructionPotentiate, description="")
        self._extractor.add_object("square", CurveCalculationInstructionSquare, description="")
        self._extractor.add_object("square_root", CurveCalculationInstructionSquareRoot, description="")
        self._extractor.add_object("log", CurveCalculationInstructionLog, description="")
        self._extractor.add_object("exp", CurveCalculationInstructionExp, description="")
        self._extractor.add_object("filter", CurveCalculationInstructionFilter, description="")
        self._extractor.add_object("scale_x", CurveCalculationInstructionScaleX, description="")
        self._extractor.add_object("scale_y", CurveCalculationInstructionScaleY, description="")
        self._extractor.add_object("min", ValueCalculationInstructionMin, description="")
        self._extractor.add_object("max", ValueCalculationInstructionMax, description="")
        self._extractor.set_name("CalculationInstruction")
        self._extractor.set_group_name("Processing.Arrk")

    def generate(self):
        super().generate()
        self.generate_instruction()

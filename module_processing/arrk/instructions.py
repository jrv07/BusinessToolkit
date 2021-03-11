from module_processing.arrk.CurveSelection import CurveSelection
from module_processing.arrk.Calculator.CurveCalculator import CurveCalculator
from module_processing.arrk.Calculator.CurveCalculatorInput import CurveCalculatorInput
from module_processing.arrk.Calculator.CurveCalculatorCurveOutput import CurveCalculatorCurveOutput
from module_processing.arrk.Calculator.Calculation.CurveCalculation import CurveCalculation
from module_processing.arrk.Calculator.Calculation.CurveCalculationInstructionFactory import \
    CurveCalculationInstructionFactory
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionAdd import \
    CurveCalculationInstructionAdd
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionDivide import \
    CurveCalculationInstructionDivide
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionExp import \
    CurveCalculationInstructionExp
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionFilter import \
    CurveCalculationInstructionFilter
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionLog import \
    CurveCalculationInstructionLog
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionMultiply import \
    CurveCalculationInstructionMultiply
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionPotentiate import \
    CurveCalculationInstructionPotentiate
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionScaleX import \
    CurveCalculationInstructionScaleX
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionSquare import \
    CurveCalculationInstructionSquare
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionSquareRoot import \
    CurveCalculationInstructionSquareRoot
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstructionSubtract import \
    CurveCalculationInstructionSubtract
from module_processing.arrk.Calculator.Calculation.Instructions.ValueCalculationInstructionMax import \
    ValueCalculationInstructionMax
from module_processing.arrk.Calculator.Calculation.Instructions.ValueCalculationInstructionMin import \
    ValueCalculationInstructionMin
from module_processing.arrk.Plot.CurveStyle import CurveStyle
from module_processing.arrk.Plot.CurveData import CurveData
from module_processing.arrk.Plot.CurveDataTable import CurveDataTable
from module_processing.arrk.Plot.CurvePlot import CurvePlot

instructions = [
    CurveSelection({}),
    CurveCalculator({}),
    CurveCalculatorInput({}),
    CurveCalculatorCurveOutput({}),
    CurveCalculation({}),
    CurveCalculationInstructionFactory({}),
    CurveCalculationInstructionAdd({}),
    CurveCalculationInstructionDivide({}),
    CurveCalculationInstructionExp({}),
    CurveCalculationInstructionFilter({}),
    CurveCalculationInstructionLog({}),
    CurveCalculationInstructionMultiply({}),
    CurveCalculationInstructionPotentiate({}),
    CurveCalculationInstructionScaleX({}),
    CurveCalculationInstructionSquare({}),
    CurveCalculationInstructionSquareRoot({}),
    CurveCalculationInstructionSubtract({}),
    ValueCalculationInstructionMax({}),
    ValueCalculationInstructionMin({}),
    CurveStyle({}),
    CurveData({}),
    CurveDataTable({}),
    CurvePlot({})
]

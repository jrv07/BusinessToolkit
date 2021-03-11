from module_processing.animator.AnimatorTask import AnimatorTask, AnimatorRun
from module_processing.animator.AnimatorSettings import AnimatorSettings
from module_processing.animator.AnimatorInstructionFactory import AnimatorInstructionFactory
from module_processing.animator.Instructions.AnimatorInstructionColor import AnimatorInstructionColor
from module_processing.animator.Instructions.AnimatorInstructionFollow import AnimatorInstructionFollow
from module_processing.animator.Instructions.AnimatorInstructionFunction import AnimatorInstructionFunction
from module_processing.animator.Instructions.AnimatorInstructionModal import AnimatorInstructionModal
from module_processing.animator.Instructions.AnimatorInstructionFunctionBar import AnimatorInstructionFunctionBar
from module_processing.animator.Instructions.AnimatorInstructionShowFunctionInfo \
    import AnimatorInstructionShowFunctionInfo
from module_processing.animator.Instructions.AnimatorInstructionAnimatorCommand import \
    AnimatorInstructionAnimatorCommand
from module_processing.animator.Instructions.AnimatorInstructionGroup import AnimatorInstructionGroup
from module_processing.animator.Instructions.AnimatorInstructionInput import AnimatorInstructionInput
from module_processing.animator.Instructions.AnimatorInstructionSetCrossSection \
    import AnimatorInstructionSetCrossSection
from module_processing.animator.Instructions.AnimatorInstructionSetImpactor import AnimatorInstructionSetImpactor
from module_processing.animator.Instructions.AnimatorInstructionSetState import AnimatorInstructionSetState
from module_processing.animator.Instructions.AnimatorInstructionSetView import AnimatorInstructionSetView
from module_processing.animator.Instructions.AnimatorInstructionWrite import AnimatorInstructionWritePicture
from module_processing.animator.Instructions.AnimatorInstructionWrite import AnimatorInstructionWriteMovie
from module_processing.animator.Instructions.AnimatorInstructionAdd import AnimatorInstructionAdd
from module_processing.animator.Instructions.AnimatorInstructionEra import AnimatorInstructionEra
from module_processing.animator.Instructions.AnimatorInstructionExtractDataAsTable \
    import AnimatorInstructionExtractNodeDataAsTable, AnimatorInstructionExtractElementDataAsTable
from module_processing.animator.AnimatorNodeValueExtraction import AnimatorNodeValueExtraction
from module_processing.animator.AnimatorElementValueExtraction import AnimatorElementValueExtraction
from module_processing.animator.Instructions.AnimatorInstructionSetLabelPosition \
    import AnimatorInstructionSetLabelPosition
from module_processing.animator.Instructions.AnimatorInstructionExtractCurveFromNodeHistory \
    import AnimatorInstructionExtractCurveFromNodeHistory
from module_processing.animator.Instructions.AnimatorInstructionExtractCurveFromHistory \
    import AnimatorInstructionExtractCurveFromHistory, AnimatorInstructionExtractBinoutFromHistory


instructions = [
    AnimatorTask({}),
    AnimatorRun({}),
    AnimatorSettings({}),
    AnimatorInstructionFactory({}),
    AnimatorInstructionAdd({}),
    AnimatorInstructionEra({}),
    AnimatorInstructionColor({}),
    AnimatorInstructionFollow({}),
    AnimatorInstructionFunction({}),
    AnimatorInstructionModal({}),
    AnimatorInstructionFunctionBar({}),
    AnimatorInstructionShowFunctionInfo({}),
    AnimatorInstructionAnimatorCommand({}),
    AnimatorInstructionGroup({}),
    AnimatorInstructionInput({}),
    AnimatorInstructionSetCrossSection({}),
    AnimatorInstructionSetImpactor({}),
    AnimatorInstructionSetState({}),
    AnimatorInstructionSetView({}),
    AnimatorInstructionWritePicture({}),
    AnimatorInstructionWriteMovie({}),
    AnimatorNodeValueExtraction({}),
    AnimatorElementValueExtraction({}),
    AnimatorInstructionExtractNodeDataAsTable({}),
    AnimatorInstructionExtractElementDataAsTable({}),
    AnimatorInstructionSetLabelPosition({}),
    AnimatorInstructionExtractCurveFromNodeHistory({}),
    AnimatorInstructionExtractCurveFromHistory({}),
    AnimatorInstructionExtractBinoutFromHistory({})
]

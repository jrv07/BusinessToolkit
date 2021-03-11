from module_processing.metapost.MetapostTask import MetapostTask, MetapostRun
from module_processing.metapost.MetapostSettings import MetapostSettings
from module_processing.metapost.MetapostInstructionFactory import MetapostInstructionFactory
from module_processing.metapost.Instructions.MetapostInstructionInput import MetapostInstructionInput
from module_processing.metapost.Instructions.MetapostInstructionAdd import MetapostInstructionAdd
from module_processing.metapost.Instructions.MetapostInstructionEra import MetapostInstructionEra
from module_processing.metapost.Instructions.MetapostInstructionGroup import MetapostInstructionGroup
from module_processing.metapost.Instructions.MetapostInstructionColor import MetapostInstructionColor
from module_processing.metapost.Instructions.MetapostInstructionSetView import MetapostInstructionSetView
from module_processing.metapost.Instructions.MetapostInstructionSetCrossSection import MetapostInstructionSetCrossSection
from module_processing.metapost.Instructions.MetapostInstructionSetState import MetapostInstructionSetState
from module_processing.metapost.Instructions.MetapostInstructionFunction import MetapostInstructionFunction
from module_processing.metapost.Instructions.MetapostInstructionModal import MetapostInstructionModal
from module_processing.metapost.Instructions.MetapostInstructionFunctionBar import MetapostInstructionFunctionBar
from module_processing.metapost.Instructions.MetapostInstructionShowFunctionInfo import \
    MetapostInstructionShowFunctionInfo
from module_processing.metapost.Instructions.MetapostInstructionSetLabelPosition import \
    MetapostInstructionSetLabelPosition
from module_processing.metapost.Instructions.MetapostInstructionWrite import MetapostInstructionWritePicture, \
    MetapostInstructionWriteMovie
from module_processing.metapost.Instructions.MetapostInstructionFollow import MetapostInstructionFollow
from module_processing.metapost.Instructions.MetapostInstructionSlotVisibility import MetapostChangeSlotVisibility
from module_processing.metapost.Instructions.MetapostInstructionExtractDataAsTable import \
    MetapostInstructionExtractNodeDataAsTable, MetapostInstructionExtractElementDataAsTable
from module_processing.metapost.Instructions.MetapostInstructionExtractFunctionInfo import \
    MetapostInstructionExtractFunctionInfo
from module_processing.metapost.Instructions.MetapostInstructionExtractCurveFromHistory import \
    MetapostInstructionExtractCurveFromNodeHistory, MetapostInstructionExtractCurveFromHistory

instructions = [
    MetapostTask({}),
    MetapostRun({}),
    MetapostSettings({}),
    MetapostInstructionFactory({}),
    MetapostInstructionInput({}),
    MetapostInstructionAdd({}),
    MetapostInstructionEra({}),
    MetapostInstructionColor({}),
    MetapostInstructionFollow({}),
    MetapostInstructionFunction({}),
    MetapostInstructionModal({}),
    MetapostInstructionFunctionBar({}),
    MetapostInstructionShowFunctionInfo({}),
    MetapostInstructionGroup({}),
    MetapostInstructionSetCrossSection({}),
    MetapostInstructionSetState({}),
    MetapostInstructionSetView({}),
    MetapostInstructionWritePicture({}),
    MetapostInstructionWriteMovie({}),
    MetapostChangeSlotVisibility({}),
    MetapostInstructionExtractFunctionInfo({}),
    MetapostInstructionExtractNodeDataAsTable({}),
    MetapostInstructionExtractElementDataAsTable({}),
    MetapostInstructionSetLabelPosition({}),
    MetapostInstructionExtractCurveFromNodeHistory({}),
    MetapostInstructionExtractCurveFromHistory({}),
]

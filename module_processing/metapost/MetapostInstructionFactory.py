from module_misc.InstructionFactory import InstructionFactory
from module_processing.metapost.Instructions.MetapostInstruction import MetapostInstruction
from module_processing.metapost.Instructions.MetapostInstructionInput import MetapostInstructionInput
from module_processing.metapost.Instructions.MetapostInstructionAdd import MetapostInstructionAdd
from module_processing.metapost.Instructions.MetapostInstructionEra import MetapostInstructionEra
from module_processing.metapost.Instructions.MetapostInstructionGroup import MetapostInstructionGroup
from module_processing.metapost.Instructions.MetapostInstructionColor import MetapostInstructionColor
from module_processing.metapost.Instructions.MetapostInstructionSetView import MetapostInstructionSetView
from module_processing.metapost.Instructions.MetapostInstructionSetCrossSection import \
    MetapostInstructionSetCrossSection
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


class MetapostInstructionFactory(InstructionFactory):
    def __init__(self, parameters):
        super().__init__(parameters, MetapostInstruction)
        self._extractor.add_object("input", MetapostInstructionInput, description="read Input data")
        self._extractor.add_object("add", MetapostInstructionAdd, description="add PIDs/Elements/Groups")
        self._extractor.add_object("era", MetapostInstructionEra, description="erase PIDs/Elements/Groups")
        self._extractor.add_object("set_color", MetapostInstructionColor, description="define colors to PIDs/Groups")
        self._extractor.add_object("set_view", MetapostInstructionSetView, description="define camera view")
        self._extractor.add_object("set_cross_section", MetapostInstructionSetCrossSection,
                                   description="define cross section")
        self._extractor.add_object("set_state", MetapostInstructionSetState, description="define state of Simulation")
        self._extractor.add_object("set_group", MetapostInstructionGroup, description="define new Group")
        self._extractor.add_object("function", MetapostInstructionFunction, description="activate Function")
        self._extractor.add_object("modal", MetapostInstructionModal, description="activate Modal analysis")
        self._extractor.add_object("function_bar", MetapostInstructionFunctionBar, description="define FringeBar")
        self._extractor.add_object("show_function_info", MetapostInstructionShowFunctionInfo,
                                   description="display Function Info")
        self._extractor.add_object("set_label_position", MetapostInstructionSetLabelPosition,
                                   description="position Annotation")
        self._extractor.add_object("write_picture", MetapostInstructionWritePicture, description="write Image out")
        self._extractor.add_object("write_movie", MetapostInstructionWriteMovie, description="write Animation out")
        self._extractor.add_object("follow", MetapostInstructionFollow, description="define Follows")
        self._extractor.add_object("set_visibility", MetapostChangeSlotVisibility, description="define Slot visibility")
        self._extractor.add_object("extract_node_data", MetapostInstructionExtractNodeDataAsTable,
                                   description="extract Information based on Node")
        self._extractor.add_object("extract_element_data", MetapostInstructionExtractElementDataAsTable,
                                   description="extract Information based on Element")
        self._extractor.add_object("extract_node_history", MetapostInstructionExtractCurveFromNodeHistory,
                                   description="extract History plot from Nodes")
        self._extractor.add_object("extract_history_plot", MetapostInstructionExtractCurveFromHistory,
                                   description="extract History plot")
        self._extractor.add_object("extract_function_info", MetapostInstructionExtractFunctionInfo,
                                   description="extract Information based on Function")
        self._extractor.set_name("MetapostInstruction")
        self._extractor.set_group_name("Processing.Metapost")

    @property
    def commands(self):
        return self._instruction.commands

    def generate(self):
        super().generate()
        self.generate_instruction()
        self._instruction.store_in_register()


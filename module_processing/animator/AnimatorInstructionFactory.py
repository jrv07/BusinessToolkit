from module_misc.InstructionFactory import InstructionFactory
from module_processing.animator.Instructions.AnimatorInstruction import AnimatorInstruction
from module_processing.animator.Instructions.AnimatorInstructionInput import AnimatorInstructionInput
from module_processing.animator.Instructions.AnimatorInstructionWrite import \
    AnimatorInstructionWritePicture, AnimatorInstructionWriteMovie
from module_processing.animator.Instructions.AnimatorInstructionFollow import AnimatorInstructionFollow
from module_processing.animator.Instructions.AnimatorInstructionFunction import AnimatorInstructionFunction
from module_processing.animator.Instructions.AnimatorInstructionModal import AnimatorInstructionModal
from module_processing.animator.Instructions.AnimatorInstructionFunctionBar import AnimatorInstructionFunctionBar
from module_processing.animator.Instructions.AnimatorInstructionShowFunctionInfo \
    import AnimatorInstructionShowFunctionInfo
from module_processing.animator.Instructions.AnimatorInstructionAnimatorCommand import \
    AnimatorInstructionAnimatorCommand
from module_processing.animator.Instructions.AnimatorInstructionGroup import AnimatorInstructionGroup
from module_processing.animator.Instructions.AnimatorInstructionAdd import AnimatorInstructionAdd
from module_processing.animator.Instructions.AnimatorInstructionEra import AnimatorInstructionEra
from module_processing.animator.Instructions.AnimatorInstructionColor import AnimatorInstructionColor
from module_processing.animator.Instructions.AnimatorInstructionSetView import AnimatorInstructionSetView
from module_processing.animator.Instructions.AnimatorInstructionSetCrossSection import \
    AnimatorInstructionSetCrossSection
from module_processing.animator.Instructions.AnimatorInstructionSetImpactor import AnimatorInstructionSetImpactor
from module_processing.animator.Instructions.AnimatorInstructionSetState import AnimatorInstructionSetState
from module_processing.animator.Instructions.AnimatorInstructionSlotVisibility import AnimatorChangeSlotVisibility
from module_processing.animator.Instructions.AnimatorInstructionExtractDataAsTable \
    import AnimatorInstructionExtractNodeDataAsTable
from module_processing.animator.Instructions.AnimatorInstructionExtractDataAsTable \
    import AnimatorInstructionExtractElementDataAsTable
from module_processing.animator.Instructions.AnimatorInstructionSetLabelPosition \
    import AnimatorInstructionSetLabelPosition
from module_processing.animator.Instructions.AnimatorInstructionExtractFunctionInfo \
    import AnimatorInstructionExtractFunctionInfo
from module_processing.animator.Instructions.AnimatorInstructionExtractCurveFromNodeHistory \
    import AnimatorInstructionExtractCurveFromNodeHistory
from module_processing.animator.Instructions.AnimatorInstructionExtractCurveFromHistory \
    import AnimatorInstructionExtractCurveFromHistory, AnimatorInstructionExtractBinoutFromHistory


class AnimatorInstructionFactory(InstructionFactory):
    def __init__(self, parameters):
        super().__init__(parameters, AnimatorInstruction)
        self._extractor.add_object("input", AnimatorInstructionInput, description="read Input data")
        self._extractor.add_object("write_picture", AnimatorInstructionWritePicture, description="write Image out")
        self._extractor.add_object("write_movie", AnimatorInstructionWriteMovie, description="write Animation out")
        self._extractor.add_object("follow", AnimatorInstructionFollow, description="define Follows")
        self._extractor.add_object("function", AnimatorInstructionFunction, description="activate Function")
        self._extractor.add_object("modal", AnimatorInstructionModal, description="activate modal analysis")
        self._extractor.add_object("function_bar", AnimatorInstructionFunctionBar, description="")
        self._extractor.add_object("show_function_info", AnimatorInstructionShowFunctionInfo,
                                   description="display Fun Info")
        self._extractor.add_object("set_label_position", AnimatorInstructionSetLabelPosition,
                                   description="position Annotation")
        self._extractor.add_object("animator_command", AnimatorInstructionAnimatorCommand,
                                   description="Animator Command")
        self._extractor.add_object("set_group", AnimatorInstructionGroup, description="define user Group")
        self._extractor.add_object("add", AnimatorInstructionAdd, description="add PIDs/Elements/Groups")
        self._extractor.add_object("era", AnimatorInstructionEra, description="erase PIDs/Elements/Groups")
        self._extractor.add_object("set_color", AnimatorInstructionColor, description="define colors to PIDs/Groups")
        self._extractor.add_object("set_view", AnimatorInstructionSetView, description="define camera view")
        self._extractor.add_object("set_cross_section", AnimatorInstructionSetCrossSection,
                                   description="define cross section")
        self._extractor.add_object("set_impactor", AnimatorInstructionSetImpactor, description="define Imp. point")
        self._extractor.add_object("set_state", AnimatorInstructionSetState, description="define state of Sim")
        self._extractor.add_object("set_visibility", AnimatorChangeSlotVisibility, description="define Slot visibility")
        self._extractor.add_object("extract_node_data", AnimatorInstructionExtractNodeDataAsTable,
                                   description="extract Information based on Node")
        self._extractor.add_object("extract_element_data", AnimatorInstructionExtractElementDataAsTable,
                                   description="extract Information based on Element")
        self._extractor.add_object("extract_node_history", AnimatorInstructionExtractCurveFromNodeHistory,
                                   description="extract History plot from Nodes")
        self._extractor.add_object("extract_curve", AnimatorInstructionExtractCurveFromHistory,
                                   description="extract Curves")
        self._extractor.add_object("extract_curve", AnimatorInstructionExtractBinoutFromHistory,
                                   description="extract Curves")
        self._extractor.add_object("extract_function_info", AnimatorInstructionExtractFunctionInfo,
                                   description="extract Information based on Function")
        self._extractor.set_name("AnimatorInstruction")
        self._extractor.set_group_name("Processing.Animator")

    @property
    def commands(self):
        return self._instruction.commands

    def generate(self):
        super().generate()
        self.generate_instruction()
        self._instruction.store_in_register()


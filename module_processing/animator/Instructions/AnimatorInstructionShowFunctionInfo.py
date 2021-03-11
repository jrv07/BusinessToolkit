from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionShowFunctionInfo(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._entity_type = None
        self._info_type = None
        valid_info_types = ["max", "min"]
        self._extractor.add_str("info_type", valid_values=valid_info_types, description="type of function info",
                                optional=False,)

    def generate_instruction(self):
        for slot in self._slots:
            self.add_slot_command(slot, "fun inf all act {}".format(self._info_type))

    def get_arguments(self):
        super().get_arguments()
        self._info_type = self._extractor.get_value("info_type")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorChangeSlotVisibility(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._hide = None
        self._show = None
        self._extractor.add_bool("show", alternative="hide", description="slot on")
        self._extractor.add_bool("hide", description="slot off")

    def generate_instruction_slot(self, slot):
        if self._hide is not None:
            self.add_slot_command(slot, "era slo act")

        if self._show is not None:
            self.add_slot_command(slot, "add slo act")

    def generate_instruction(self):
        for slot in self._slots:
            self.generate_instruction_slot(slot)

    def get_arguments(self):
        super().get_arguments()
        self._show = self._extractor.get_value("show")
        self._hide = self._extractor.get_value("hide")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
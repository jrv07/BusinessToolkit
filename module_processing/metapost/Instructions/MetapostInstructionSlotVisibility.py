from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostChangeSlotVisibility(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._hide = False
        self._show = False
        self._extractor.add_bool("show", description="slot on")
        self._extractor.add_bool("hide", description="slot off")

    def generate_instruction_slot(self, slot):
        if self._hide is True:
            self.add_command("model hide {}".format(slot))

        if self._show is True:
            self.add_command("model show {}".format(slot))

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
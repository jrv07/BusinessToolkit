from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionModal(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._mode = None
        self._scale = None
        self._extractor.add_int("mode", description="mode_ID")
        self._extractor.add_float("scale", optional=False, description="scale factor")

    def generate_instruction(self):
        for slot in self._slots:
            self.add_slot_command(slot, 'states sort ascending mode')
            self.add_slot_command(slot, 'states gendel {}'.format(self._mode - 1))
            self.add_slot_command(slot, 'option state {}'.format(self._mode))
            self.add_slot_command(slot, 'displ scale {}'.format(self._scale))
            self.add_slot_command(slot, 'animation autogen enable')
            self.add_slot_command(slot, 'states winlock act {}'.format(self._mode))

    def get_arguments(self):
        super().get_arguments()
        self._mode = self._extractor.get_value("mode")
        self._scale = self._extractor.get_value("scale")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

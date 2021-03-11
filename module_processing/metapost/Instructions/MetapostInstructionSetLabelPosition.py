from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionSetLabelPosition(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._x = None
        self._y = None
        self._extractor.add_float("x", optional=False, description="x position")
        self._extractor.add_float("y", optional=False, description="y position")

    def generate_instruction(self):
        for slot in self._slots:
            self.add_slot_command(slot, "annotation position 1 setxy {} {} act".format(self._x, self._y))

    def get_arguments(self):
        super().get_arguments()
        self._x = self._extractor.get_value("x")
        self._y = self._extractor.get_value("y")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionSetState(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._state = None
        state_values = ["first"]
        self._extractor.add_str("state", alternative="state_id", valid_values=state_values,
                                description="state as string")
        self._extractor.add_int("state_id", specifier="state", description="state_ID")

    def generate_instruction(self):
        for slot in self._slots:
            if self._state is not None:
                self.add_slot_command(slot, "option state {}".format(self._state))

    def get_state(self):
        self._state = self._extractor.get_value("state")
        if self._state is None:
            self._state = self._extractor.get_value("state_id")

    def get_arguments(self):
        super().get_arguments()
        self.get_state()

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

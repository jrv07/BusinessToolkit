from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionSetState(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._state = None  # parameters.get('state', None)  # Enter fir/las/nex/pre/fmi/fma
        self._state_time = None  # parameters.get('state_time', None)  # Enter state-time)
        self._label_name = None  # parameters.get('label_name', None) # format lable for picture
        state_values = ["fir", "las", "nex", "pre", "fmi", "fma"]
        self._extractor.add_str("state", alternative="state_id", valid_values=state_values,
                                description="state as string")
        self._extractor.add_int("state_id", specifier="state", description="state_ID")
        self._extractor.add_float("state_time", description="sim time")
        self._extractor.add_str("label_name", description="activate sim time/state label")

    def generate_instruction(self):
        for slot in self._slots:
            if self._state is not None:
                self.add_slot_command(slot, "sta set {}".format(self._state))

            if self._state_time is not None:
                self.add_slot_command(slot, "sta set tim {}".format(str(self._state_time)))

            if self._label_name is not None:
                self.add_slot_command(slot, "sta fms on")
                self.add_slot_command(slot, 'sta fms tra set "{}"'.format(self._label_name))

    def get_state(self):
        self._state = self._extractor.get_value("state")
        if self._state is None:
            self._state = self._extractor.get_value("state_id")

    def get_arguments(self):
        super().get_arguments()
        self.get_state()
        self._state_time = self._extractor.get_value("state_time")
        self._label_name = self._extractor.get_value("label_name")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()


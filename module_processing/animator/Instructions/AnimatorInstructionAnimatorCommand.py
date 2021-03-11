from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionAnimatorCommand(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._user_command = None
        self._read_session = None
        self._extractor.add_list("user_command", entry_type=str, optional=True, description="animator command")
        self._extractor.add_str("read_session", optional=True, description="animator session")

    def generate_instruction(self):
        for slot in self._slots:
            if self._user_command is not None:
                for item in self._user_command:
                    self.add_slot_command(slot, "{}".format(item))

    def get_arguments(self):
        super().get_arguments()
        self._user_command = self._extractor.get_value("user_command")
        self._read_session = self._extractor.get_value("read_session")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()
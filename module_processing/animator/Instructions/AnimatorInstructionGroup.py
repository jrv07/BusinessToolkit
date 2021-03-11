from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionGroup(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._group_name = None
        self._user_command = None
        self._extractor.add_str("group_name", optional=False, description="group name")
        self._extractor.add_list("user_command", entry_type=str, optional=True, description="user command")

    def generate_instruction(self):
        for slot in self._slots:
            if self._user_command is not None:
                for item in self._user_command:
                    self.add_slot_command(slot, "{}".format(item))
            if self._group_name is not None:
                self.add_slot_command(slot, "gro rde {}".format(self._group_name))

    def get_arguments(self):
        super().get_arguments()
        self._group_name = self._extractor.get_value("group_name")
        self._user_command = self._extractor.get_value("user_command")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

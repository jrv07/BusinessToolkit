from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionFunction(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._function = None
        self._deform = None
        self._un_deform = None
        self._user_command = None
        self._extractor.add_str("function", description="function_name")
        valid_deform_values = ["uno", "dno", "vno", "wno", "uel", "del", "vel", "wel"]
        self._extractor.add_str("deform", valid_values=valid_deform_values, default="off",
                                description="type of deformation")
        self._extractor.add_bool("undeform", optional=False, default=False, description="deformation on/off")
        self._extractor.add_list("user_command", entry_type=str, optional=True, description="user command")

    def generate_instruction(self):
        for slot in self._slots:
            if self._function is not None:
                self.add_slot_command(slot, 'fun act "{}"'.format(self._function))
                self.add_slot_command(slot, "sty fun ele all")
                self.add_slot_command(slot, 'txt fba add "{}"'.format(self._function))
            else:
                self.add_slot_command(slot, "sty fun off all")
                if self._deform:
                    self.add_slot_command(slot, "sty int {} all".format(self._deform))
                    self.add_slot_command(slot, 'txt fba add "Displacement"')

            if self._un_deform:
                self.add_slot_command(slot, "opt udg sta 1st")

            if self._user_command is not None:
                for item in self._user_command:
                    self.add_slot_command(slot, "{}".format(item))

    def get_arguments(self):
        super().get_arguments()
        self._function = self._extractor.get_value("function")
        self._deform = self._extractor.get_value("deform")
        self._un_deform = self._extractor.get_value("undeform")
        self._user_command = self._extractor.get_value("user_command")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

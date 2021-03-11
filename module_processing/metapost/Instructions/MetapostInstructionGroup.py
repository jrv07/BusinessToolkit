from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionGroup(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._group_name = None
        self._extractor.add_str("group_name", optional=False, description="group_name")

    def generate_instruction(self):
        for slot in self._slots:
            if self._group_name is not None:
                self.add_slot_command(slot, 'gro def {}'.format(self._group_name))

    def get_arguments(self):
        super().get_arguments()
        self._group_name = self._extractor.get_value("group_name")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

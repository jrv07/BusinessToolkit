from module_processing.metapost.Instructions.MetapostInstruction import MetapostInstruction


class MetapostInstructionSlotDependent(MetapostInstruction):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._slots = None
        self._extractor.add_list("slots_list", specifier="slots", entry_type=int, optional=False,
                                 alternative="slots_str", description="slot as list")
        self._extractor.add_str("slots_str", specifier="slots", valid_values=["all"], optional=False, default="all",
                                description="slot as string")

    @staticmethod
    def generate_instruction_line(slot, instruction):
        return '{}:{}'.format(slot, instruction)

    def add_slot_command(self, slot, instruction):
        self.add_command('{}:{}'.format(slot, instruction))

    def generate_slots(self):
        slots_list = self._extractor.get_value("slots_list")
        if slots_list is None:
            self._slots = [self._extractor.get_value("slots_str")]
        else:
            self._slots = slots_list

    def get_arguments(self):
        super().get_arguments()
        self.generate_slots()

    def generate(self):
        super().generate()

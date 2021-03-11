from module_processing.animator.Instructions.AnimatorInstruction import AnimatorInstruction


class AnimatorInstructionSlotDependent(AnimatorInstruction):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._slots = None
        self._extractor.add_list("slots_list", specifier="slots", entry_type=int, optional=False,
                                 alternative="slots_str", description="slot as list")
        self._extractor.add_str("slots_str", specifier="slots", valid_values=["all"], optional=False, default="all",
                                description="slot as string")

    #def generate_instruction_header(self):
    #    if self._slots is not None:
    #        self.add_command('v["Model"]:!era slo all')
    #        for slot in self._slots:
    #            self.add_command('v["Model"]:!add slo {}'.format(slot))

    #def generate_instruction_footer(self):
    #    self._commands.extend([
    #        'v["Model"]:!add slo all',
    #        'v["Model"]:!vie res',
    #        'v["Model"]:!crx swi off',
    #        'v["Model"]:!ide res',
    #        'v["Model"]:!opt udg off',
    #        'v["Model"]:!sty fun off all',
    #        'v["Model"]:!imp usr del all'])

    @staticmethod
    def generate_instruction_line(slot, instruction):
        return 's[{}]v["Model"]:!{}'.format(slot, instruction)

    def add_slot_command(self, slot, instruction):
        self.add_command('s[{}]v["Model"]:!{}'.format(slot, instruction))

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

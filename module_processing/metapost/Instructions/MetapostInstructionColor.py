from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionColor(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._col_bac = None
        self._col_pid = None
        self._col_lay = None
        self._col_gro = None
        self._extractor.add_str("col_bac", description="background color")
        self._extractor.add_str("col_pid", description="part_ID color")
        self._extractor.add_str("col_lay", description="layer_name color")
        self._extractor.add_str("col_gro", description="group_name color")

    def add_slot_color_command(self, slot, to_colorize, color):
        self.add_slot_command(slot, "grstyle scalarfringe disable")
        self.add_slot_command(slot, "col {} {}".format(to_colorize, color))

    def add_slot_color_pid_command(self, slot, color):
        self.add_slot_command(slot, "grstyle scalarfringe disable")
        self.add_slot_command(slot, "col pid {} act".format(color))

    def generate_instruction_slot(self, slot):
        if self._col_bac is not None:
            self.add_slot_color_command(slot, "bac", self._col_bac)

        if self._col_pid is not None:
            self.add_slot_color_pid_command(slot, self._col_pid)

        if self._col_lay is not None:
            self.add_slot_color_command(slot, "lay", self._col_lay)

        if self._col_gro is not None:
            self.add_slot_color_command(slot, "gro", self._col_gro)

    def generate_instruction(self):
        for slot in self._slots:
            self.generate_instruction_slot(slot)

    def get_arguments(self):
        super().get_arguments()
        self._col_bac = self._extractor.get_value("col_bac")
        self._col_pid = self._extractor.get_value("col_pid")
        self._col_lay = self._extractor.get_value("col_lay")
        self._col_gro = self._extractor.get_value("col_gro")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

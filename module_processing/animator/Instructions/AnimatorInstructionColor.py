from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionColor(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._col_bac = None
        self._col_ove = None
        self._col_pid = None
        self._col_lay = None
        self._col_gro = None
        self._col_crs = None
        self._col_udg = None
        self._udg = None
        self._col_tra = None
        self._user_command = None
        self._extractor.add_str("col_bac", description="background colo")
        self._extractor.add_str("col_ove", description="text color")
        self._extractor.add_str("col_pid", description="part_ID color")
        self._extractor.add_str("col_lay", description="layer_name color")
        self._extractor.add_str("col_gro", description="group_name color")
        self._extractor.add_str("col_crs", description="cross section name color")
        self._extractor.add_str("col_udg", description="undeformed geometry color")
        self._extractor.add_bool("udg", description="undeformed geometry on/off")
        self._extractor.add_str("col_tra", description="transperancy factor")
        self._extractor.add_list("user_command", entry_type=str, optional=True, description="user command")

    def add_slot_color_command(self, slot, to_colorize, color):
        self.add_slot_command(slot, "col {} {}".format(to_colorize, color))

    def add_slot_color_pid_command(self, slot, color):
        self.add_slot_command(slot, "col pid {} act".format(color))

    def generate_instruction_slot(self, slot):
        if self._col_bac is not None:
            self.add_slot_color_command(slot, "bac", self._col_bac)

        if self._col_ove is not None:
            self.add_slot_color_command(slot, "ove", self._col_ove)

        if self._col_pid is not None:
            self.add_slot_color_pid_command(slot, self._col_pid)

        if self._col_lay is not None:
            self.add_slot_color_command(slot, "lay", self._col_lay)

        if self._col_crs is not None:
            self.add_slot_color_command(slot, "crs", self._col_crs)

        if self._col_udg is not None:
            self.add_slot_color_command(slot, "udg", self._col_udg)

        if self._udg is not None:
            self.add_slot_command(slot, "opt udg {}".format(self.get_on_off(self._udg)))

        if self._col_tra is not None:
            self.add_slot_color_command(slot, "tra", self._col_tra)

        for slot in self._slots:
            if self._user_command is not None:
                for item in self._user_command:
                    self.add_slot_command(slot, "{}".format(item))

    def generate_instruction(self):
        for slot in self._slots:
            self.generate_instruction_slot(slot)

    def get_arguments(self):
        super().get_arguments()
        self._col_bac = self._extractor.get_value("col_bac")
        self._col_ove = self._extractor.get_value("col_ove")
        self._col_pid = self._extractor.get_value("col_pid")
        self._col_lay = self._extractor.get_value("col_lay")
        self._col_gro = self._extractor.get_value("col_gro")
        self._col_crs = self._extractor.get_value("col_crs")
        self._col_udg = self._extractor.get_value("col_udg")
        self._col_tra = self._extractor.get_value("col_tra")
        self._user_command = self._extractor.get_value("user_command")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()


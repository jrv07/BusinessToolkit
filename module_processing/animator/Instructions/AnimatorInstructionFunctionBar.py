from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionFunctionBar(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._fba_num = None
        self._fba_range = None
        self._fba_col = None
        self._fba_fmt = None
        self._fba_era_col = None
        self._fba_add = None
        self._fba_era = None
        self._user_command = None
        self._extractor.add_int("fba_num", description="number of function values")
        self._extractor.add_list("fba_range", entry_type=float, length=2, description="range min/max")
        self._extractor.add_list("fba_col", entry_type=str, length=2, description="")
        self._extractor.add_float("fba_fmt", description="function value accuracy")
        self._extractor.add_int("fba_add", description="function value add")
        self._extractor.add_int("fba_era", description="function value erase")
        self._extractor.add_list("user_command", entry_type=str, optional=True, description="user command")

    def generate_instruction(self):
        for slot in self._slots:
            if self._fba_num is not None:
                self.add_slot_command(slot, "fun fba num {}".format(str(self._fba_num)))

            if self._fba_range is not None:
                self.add_slot_command(slot, "fun fba ran {} {}"
                                      .format(str(self._fba_range[0]), str(self._fba_range[1])))

            if self._fba_col is not None:
                self.add_slot_command(slot, "fun fba col {} {}"
                                      .format(str(self._fba_col[0]), str(self._fba_col[1])))

            if self._fba_fmt is not None:
                self.add_slot_command(slot, "fun fba fmt {}f".format(str(self._fba_fmt)))

            if self._fba_add is not None:
                self.add_slot_command(slot, "fun fba add {}".format(str(self._fba_add)))

            if self._fba_era is not None:
                self.add_slot_command(slot, "fun fba del {}".format(str(self._fba_era)))

            if self._user_command is not None:
                for item in self._user_command:
                    self.add_slot_command(slot, "{}".format(item))

    def get_arguments(self):
        super().get_arguments()
        self._fba_num = self._extractor.get_value("fba_num")
        self._fba_range = self._extractor.get_value("fba_range")
        self._fba_col = self._extractor.get_value("fba_col")
        self._fba_fmt = self._extractor.get_value("fba_fmt")
        self._fba_add = self._extractor.get_value("fba_add")
        self._fba_era = self._extractor.get_value("fba_era")
        self._user_command = self._extractor.get_value("user_command")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

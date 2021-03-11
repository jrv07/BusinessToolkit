from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionFunctionBar(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._fba_num = None
        self._fba_font = None
        self._fba_range = None
        self._fba_novalue_col = None
        self._fba_value = None
        self._extractor.add_int("fba_num", description="function value accuracy")
        valid_fonts = ["Arial", "Calibri"]
        self._extractor.add_str("fba_font", valid_values=str(valid_fonts), description="font type")
        self._extractor.add_list("fba_range", entry_type=float, length=2, description="range min/max")
        self._extractor.add_bool("fba_novalue_col", optional=False, default=False, description="function color on/off")
        self._extractor.add_bool("fba_value", optional=False, default=True, description="function value on/off")

    def generate_instruction(self):
        for slot in self._slots:
            if self._fba_num is not None:
                self.add_slot_command(slot, "options fringebar format enabled fixed")
                self.add_slot_command(slot, "options fringebar format enabled digits {}".format(str(self._fba_num)))
                self.add_slot_command(slot, "options fringebar font values {}".format(str(self._fba_font)))

            if self._fba_range is not None:
                self.add_slot_command(slot, "srange set {}, {}"
                                      .format(str(self._fba_range[0]), str(self._fba_range[1])))

            if self._fba_novalue_col is False:
                self.add_slot_command(slot, "options fringe mode novaluecolor enabled off")
            else:
                self.add_slot_command(slot, "options fringe mode novaluecolor enabled on")

            if self._fba_value is False:
                self.add_slot_command(slot, "options fringe visibility values enabled off")
            else:
                self.add_slot_command(slot, "options fringe visibility values enabled on")

    def get_arguments(self):
        super().get_arguments()
        self._fba_num = self._extractor.get_value("fba_num")
        self._fba_font = self._extractor.get_value("fba_font")
        self._fba_range = self._extractor.get_value("fba_range")
        self._fba_novalue_col = self._extractor.get_value("fba_novalue_col")
        self._fba_value = self._extractor.get_value("fba_value")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

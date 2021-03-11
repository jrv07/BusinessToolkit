from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionEra(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._pid = None  # [21000000, 11000000-15999999] # Pid or Pid range
        self._lay = None  # [RK, TUEREN] # layer name
        self._gro = None  # [group_rk, group_dummy] # group name
        self._ele = None
        self._ele_type = None
        self._extractor.add_list("pid", entry_type=str, description="part_ID")
        self._extractor.add_list("lay", entry_type=str, description="layer_name")
        self._extractor.add_list("gro", entry_type=str, description="group_name")
        self._extractor.add_list("ele", entry_type=str, description="element_ID")
        valid_ele_types = ["bar", "rbe", "cfr", "mas", "mpc", "bea", "for", "spc"]
        self._extractor.add_list("ele_type", entry_type=str, valid_values=list(valid_ele_types),
                                 description="type of element")

    def generate_instruction(self):
        for slot in self._slots:
            if self._pid is not None:
                for pid in self._pid:
                    self.add_slot_command(slot, "era pid {}".format(str(pid)))

            if self._lay is not None:
                for lay in self._lay:
                    self.add_slot_command(slot, "era lay {}".format(str(lay)))

            if self._gro is not None:
                for gro in self._gro:
                    self.add_slot_command(slot, "era gro {}".format(str(gro)))

            if self._ele is not None:
                for ele in self._ele:
                    self.add_slot_command(slot, "era ele {}".format(str(ele)))

            if self._ele_type is not None:
                for ele_type in self._ele_type:
                    self.add_slot_command(slot, "era {} all".format(str(ele_type)))

    def get_arguments(self):
        super().get_arguments()
        self._pid = self._extractor.get_value("pid")
        self._lay = self._extractor.get_value("lay")
        self._gro = self._extractor.get_value("gro")
        self._ele = self._extractor.get_value("ele")
        self._ele_type = self._extractor.get_value("ele_type")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()

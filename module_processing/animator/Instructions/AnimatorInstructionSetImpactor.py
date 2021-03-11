from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionSetImpactor(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._imp_point = None  # parameters.get("imp_point", None)
        self._imp_name = None  # parameters.get("imp_name", None)
        self._imp_style = None  # parameters.get("imp_style", None)
        self._imp_radius = None  # parameters.get("imp_radi", None)
        self._extractor.add_int("imp_point", description="select impact point node_ID/element_ID")
        self._extractor.add_str("imp_name", description="impact point name")
        valid_imp_styles = ["2d", "3d", "fix", "fof", "fon", "mod", "nor", "top"]
        self._extractor.add_list("imp_style", entry_type=str, valid_values=valid_imp_styles, description="style 2D/3D")
        self._extractor.add_float("imp_radius", description="radius")

    def generate_instruction(self):
        for slot in self._slots:
            if self._imp_point is not None:
                self.add_slot_command(slot, "add ele nod {}".format(str(self._imp_point)))

                if self._imp_name is not None:
                    self.add_slot_command(slot, "imp usr cre {} {}".format(str(self._imp_point), self._imp_name))
                    self.add_slot_command(slot, "ide imp fms set {}".format(self._imp_name))
                    self.add_slot_command(slot, "ide imp act")
                else:
                    self.add_slot_command(slot, "imp usr cre {}".format(str(self._imp_point)))

            if self._imp_style is not None:
                for style_entry in self._imp_style:
                    self.add_slot_command(slot, "imp usr sty {} all".format(style_entry))

            if self._imp_radius is not None:
                self.add_slot_command(slot, "opt ira {}".format(str(self._imp_radius)))

    def get_arguments(self):
        super().get_arguments()
        self._imp_point = self._extractor.get_value("imp_point")
        self._imp_name = self._extractor.get_value("imp_name")
        self._imp_style = self._extractor.get_value("imp_style")
        self._imp_radius = self._extractor.get_value("imp_radius")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()


from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionSetLabelPosition(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._label_type = None
        self._info_type = None
        self._x = None
        self._y = None
        valid_entity_types = ["element", "node"]
        self._extractor.add_str("label_type", valid_values=valid_entity_types, description="type of label")
        self._extractor.add_float("x", optional=False, description="x position")
        self._extractor.add_float("y", optional=False, description="y position")

    def get_label_type(self):
        label_types_dict = {
            "node": "nod",
            "element": "ele"
        }
        label_type = self._extractor.get_value("label_type")
        self._label_type = label_types_dict[label_type]

    def generate_instruction(self):
        for slot in self._slots:
            self.add_slot_command(slot, "ide lof {} {} {} act".format(self._x, self._y, self._label_type))

    def get_arguments(self):
        super().get_arguments()
        self.get_label_type()
        self._x = self._extractor.get_value("x")
        self._y = self._extractor.get_value("y")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

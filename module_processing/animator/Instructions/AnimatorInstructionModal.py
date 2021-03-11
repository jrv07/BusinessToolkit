from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionModal(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._mode = None
        self._frame_type = None
        self._scale = None
        self._frames = None
        self._degrees = None
        self._extractor.add_int("mode", description="mode_ID")
        self._extractor.add_str("type", optional=False, description="type of animation")
        self._extractor.add_float("scale", optional=False, description="scale factor")
        self._extractor.add_int("frames", optional=False, description="no of frames")
        self._extractor.add_int("degrees", optional=False, description="angle in degree")

    def generate_instruction(self):
        for slot in self._slots:
            self.add_slot_command(slot, 'sta swi {}'.format(self._mode))
            self.add_slot_command(slot, 'dis ani all {} {} {}'.format(self._frame_type, self._frames, self._degrees))
            self.add_slot_command(slot, 'dis scs all {}'.format(self._scale))

    def get_arguments(self):
        super().get_arguments()
        self._mode = self._extractor.get_value("mode")
        self._frame_type = self._extractor.get_value("type")
        self._scale = self._extractor.get_value("scale")
        self._frames = self._extractor.get_value("frames")
        self._degrees = self._extractor.get_value("degrees")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

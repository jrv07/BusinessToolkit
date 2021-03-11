from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionFunction(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._function = None
        self._deform = None
        self._deform_off = None
        self._title_off = None
        self._delete_annotation = None
        self._extractor.add_str("function", description="function_name")
        valid_deform_values = ["unode", "dnode", "vnode", "wnode"]
        self._extractor.add_str("deform", valid_values=valid_deform_values, default="off",
                                description="type of deformation")
        self._extractor.add_bool("deform_off", optional=False, default=False, description="deformation on/off")
        self._extractor.add_bool("title_off", default=False, description="title on/off")
        self._extractor.add_bool("delete_annotation", default=False, description="annotation on/off")

    def generate_instruction(self):
        for slot in self._slots:
            if self._function is not None:
                self.add_slot_command(slot, "grstyle scalarfringe enable")
                self.add_slot_command(slot, "grstyle scalarfringe cplot")
                self.add_slot_command(slot, "grstyle scalarfringe elemdata")
                self.add_slot_command(slot, 'function scalar label {} "{}"'.format(slot, self._function))
                self.add_slot_command(slot, 'opt fringe settext title enabled "{}"'.format(self._function))
            else:
                if self._deform:
                    self.add_slot_command(slot, "grstyle scalarfringe enable")
                    self.add_slot_command(slot, "grstyle scalarfringe cplot")
                    self.add_slot_command(slot, "grstyle scalarfringe onnode")
                    self.add_slot_command(slot, "grstyle scalarfringe {}".format(self._deform))
                    self.add_slot_command(slot, 'opt fringe settext title enabled "Displacement"')

            if self._deform_off is True:
                self.add_slot_command(slot, "grstyle deform off")
            else:
                self.add_slot_command(slot, "grstyle deform on")

            if self._title_off is True:
                self.add_slot_command(slot, "option title off")
            else:
                self.add_slot_command(slot, "option title on")

            if self._delete_annotation is True:
                self.add_slot_command(slot, "annotation del visible")

    def get_arguments(self):
        super().get_arguments()
        self._function = self._extractor.get_value("function")
        self._deform = self._extractor.get_value("deform")
        self._deform_off = self._extractor.get_value("deform_off")
        self._title_off = self._extractor.get_value("title_off")
        self._delete_annotation = self._extractor.get_value("delete_annotation")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionFollow(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._follow_nodes = None
        self._status = None
        self._extractor.add_list("nodes", entry_type=int, length=3, optional=False, description="node_ID")
        self._extractor.add_bool("status", optional=False, default=True, description="follow on/off")

    def generate_instruction(self):
        for slot in self._slots:
            nodes = map(lambda node: str(node), self._follow_nodes)
            self.add_slot_command(slot, "view fo3 {}".format(",".join(nodes)))

            if not self._status:
                self.add_slot_command(slot, "view fof")

    def get_arguments(self):
        super().get_arguments()
        self._status = self._extractor.get_value("status")
        self._follow_nodes = self._extractor.get_value("nodes")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

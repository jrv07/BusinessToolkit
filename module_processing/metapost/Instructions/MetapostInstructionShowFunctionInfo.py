from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionShowFunctionInfo(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._info_type = None
        self._entity_type = None
        self._enetity_id = None
        self._reset = None
        self._annotation = None
        self._annotation_type = None
        self._annotation_type = None
        self._prefix = None
        self._suffix = None
        self._text = None
        self._precision = None
        valid_info_types = ["max", "min"]
        self._extractor.add_str("info_type", valid_values=valid_info_types, description="information type",
                                optional=False)
        valid_entity_types = ["all", "visible"]
        self._extractor.add_str("entity_type", valid_values=valid_entity_types, description="entity type")
        self._extractor.add_int("entity_id", description="element_ID or node_ID")
        valid_annotations = ["id", "value"]
        self._extractor.add_str("annotation", optional=False, valid_values=valid_annotations,
                                description="element_ID or node_ID")
        valid_annotation_types = ["element", "node"]
        self._extractor.add_str("annotation_type", optional=False, valid_values=valid_annotation_types,
                                description="element or node")
        self._extractor.add_str("prefix", default="", description="add prefix")
        self._extractor.add_str("suffix", default="", description="add suffix")
        self._extractor.add_str("text", description="user text")
        self._extractor.add_int("precision", description="accuracy")
        self._extractor.add_bool("reset", default=False, description="reset selection")

    def get_annotation(self):
        annotations_dict = {
            "value": "$val",
            "id": "$id"
        }
        annotation = self._extractor.get_value("annotation")
        self._annotation = annotations_dict[annotation]

    def get_annotation_type(self):
        annotation_types_dict = {
            "node": "visnodalids",
            "element": "elem"
        }
        annotation_type = self._extractor.get_value("annotation_type")
        self._annotation_type = annotation_types_dict[annotation_type]

    def generate_instruction(self):
        for slot in self._slots:
            if self._info_type is not None:
                self.add_command("!function info filter min off")
                self.add_command("!function info filter max off")
                self.add_command("!function info filter scalar{} on".format(self._info_type))

            if self._info_type or self._enetity_id is not None:
                self.add_slot_command(slot, "function info {}".format(self._entity_type or self._enetity_id))

            if self._annotation is not None:
                self.add_slot_command(slot, 'annotation add on{} identified "{} {} {}"'
                                      .format(self._annotation_type, self._prefix, self._annotation, self._suffix))
            if self._text is not None:
                self.add_slot_command(slot, 'annotation text 1 text "{}"'.format(self._text))

            if self._precision is not None:
                self.add_slot_command(slot, "annotation text 1 precision {}".format(self._precision))
                self.add_slot_command(slot, "annotation background 1 color auto off")
                self.add_slot_command(slot, "annotation border 1 color black")

            if self._reset is True:
                self.add_slot_command(slot, "ide res")

    def get_arguments(self):
        super().get_arguments()
        self.get_annotation()
        self.get_annotation_type()
        self._info_type = self._extractor.get_value("info_type")
        self._entity_type = self._extractor.get_value("entity_type")
        self._enetity_id = self._extractor.get_value("entity_id")
        self._prefix = self._extractor.get_value("prefix")
        self._suffix = self._extractor.get_value("suffix")
        self._text = self._extractor.get_value("text")
        self._precision = self._extractor.get_value("precision")
        self._reset = self._extractor.get_value("reset")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

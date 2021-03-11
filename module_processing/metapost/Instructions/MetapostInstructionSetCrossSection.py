from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionSetCrossSection(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._crs_name = None
        self._crs_origin = None
        self._crs_vector = None
        self._crs_visibility = None
        self._crs_default = None
        self._extractor.add_str("name", description="cross section name")
        self._extractor.add_list("origin", entry_type=float, length=3, description="cross section position")
        self._extractor.add_list("vector", entry_type=int, length=3, description="cross section vector/direction")
        self._extractor.add_bool("visibility", optional=False, default=True, description="cross section on/off")
        valid_crs_plane = ["xy", "xz", "yx", "yz", "zx", "zy"]
        self._extractor.add_str("default", valid_values=str(valid_crs_plane), default="off",
                                description="pre defined cross section")

    def generate_instruction(self):
        for slot in self._slots:
            if self._crs_name and self._crs_origin and self._crs_vector is not None:
                origin = list(map(lambda origin_entry: str(origin_entry), self._crs_origin))
                vector = list(map(lambda vector_entry: str(vector_entry), self._crs_vector))
                self.add_slot_command(slot, "plane delete all")
                self.add_slot_command(slot, "plane new {} xyz {} {}"
                                      .format(self._crs_name, "/".join(origin), "/".join(vector)))
                self.add_slot_command(slot, "plane options onlysection enable {}".format(self._crs_name))

            if self._crs_visibility is not None:
                self.add_slot_command(slot, "plane {} \"MetaPost\" {}"
                                      .format(self.get_on_off(self._crs_visibility), self._crs_name))

            if self._crs_default is not None:
                default_crs_dict = {
                    "xy": "DEFAULT_PLANE_XY",
                    "xz": "DEFAULT_PLANE_XZ",
                    "yx": "DEFAULT_PLANE_YX",
                    "yz": "DEFAULT_PLANE_YZ",
                    "zx": "DEFAULT_PLANE_ZX",
                    "zy": "DEFAULT_PLANE_ZY",
                }
                default_crs_name = default_crs_dict[self._crs_default]
                self.add_slot_command(slot, "plane delete all")
                self.add_slot_command(slot, "plane new default {}".format(self._crs_default))
                self.add_slot_command(slot, "plane options onlysection enable {}".format(default_crs_name))

    def get_arguments(self):
        super().get_arguments()
        self._crs_name = self._extractor.get_value("name")
        self._crs_origin = self._extractor.get_value("origin")
        self._crs_vector = self._extractor.get_value("vector")
        self._crs_visibility = self._extractor.get_value("visibility")
        self._crs_default = self._extractor.get_value("default")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

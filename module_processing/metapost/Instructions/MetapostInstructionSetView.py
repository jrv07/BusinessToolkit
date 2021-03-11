from module_processing.metapost.Instructions.MetapostInstructionSlotDependent import MetapostInstructionSlotDependent


class MetapostInstructionSetView(MetapostInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._xcm_siz = None
        self._vie_cam_pos = None
        self._vie_cam_reference = None
        self._vie_cam_upvector = None
        self._vie_cen = None
        self._vie_res = None
        self._vie_scale = None
        self._fn_display = None
        self._view_default = None
        self._view_file = None
        self._extractor.add_list("windows_size", entry_type=int, length=2, optional=False, default=[900, 600],
                                 description="window size")
        self._extractor.add_list("camera_position", entry_type=float, length=3, description="camera position")
        self._extractor.add_list("camera_reference", entry_type=float, length=3, description="camera reference")
        self._extractor.add_list("camera_upvector", entry_type=float, length=3, description="camera direction/vector")
        self._extractor.add_bool("center_view", description="view centre on/off")
        self._extractor.add_bool("reset_view", description="view reset on/off")
        self._extractor.add_float("zoom", description="zoom factor in/out")
        display_type = ["wire"]
        self._extractor.add_str("display", valid_values=display_type, description="display geo/mesh")
        valid_views = ["xy", "xz", "yz", "-xy", "-xz", "-yz", "iso"]
        self._extractor.add_str("default", valid_values=str(valid_views), description="use pre defined view")
        self._extractor.add_str("view_file", description="import view from external text file")

    def generate_instruction(self):
        for slot in self._slots:
            self.add_slot_command(slot, "window size {}, {}".format(str(self._xcm_siz[0]), str(self._xcm_siz[1])))

            if self._vie_cam_pos is not None:
                coord = list(map(lambda coord_entry: str(coord_entry), self._vie_cam_pos))
                self.add_slot_command(slot, "view cam pos xyz {}".format(" ".join(coord)))

            if self._vie_cam_reference is not None:
                reference = list(map(lambda reference_entry: str(reference_entry), self._vie_cam_reference))
                self.add_slot_command(slot, "view camera reference xyz {}".format(" ".join(reference)))

            if self._vie_cam_upvector is not None:
                vec = list(map(lambda vec_entry: str(vec_entry), self._vie_cam_upvector))
                self.add_slot_command(slot, "view camera upvector {}".format(" ".join(vec)))

            if self._vie_cen is not None:
                if self._vie_cen:
                    self.add_slot_command(slot, "view cen")

            if self._vie_res is not None:
                if self._vie_res:
                    self.add_slot_command(slot, "view reset")

            if self._vie_scale is not None:
                self.add_slot_command(slot, "view scale {}".format(str(self._vie_scale)))

            if self._fn_display is not None:
                self.add_slot_command(slot, "grstyle {} on".format(self._fn_display))

            if self._fn_display is None:
                self.add_slot_command(slot, "grstyle wire off".format(self._fn_display))

            if self._view_default is not None:
                default_view_dict = {
                    "xy": "DEFAULT_VIEW_:_+X+Y_(F1)",
                    "xz": "DEFAULT_VIEW_:_+X+Z_(F5)",
                    "yz": "DEFAULT_VIEW_:_+Y+Z_(F4)",
                    "-xy": "DEFAULT_VIEW_:_-X+Y_(F2)",
                    "-xz": "DEFAULT_VIEW_:_-X+Z_(F6)",
                    "-yz": "DEFAULT_VIEW_:_-Y+Z_(F3)",
                    "iso": "DEFAULT_VIEW_:_Isometric_(F10)",
                }
                default_view_name = default_view_dict[self._view_default]
                self.add_slot_command(slot, "view reset")
                self.add_slot_command(slot, 'view load "{}"'.format(default_view_name))

            if self._view_file is not None:
                self.add_slot_command(slot, "view reset")
                self.add_slot_command(slot, 'view file load "{}"'.format(self._view_file))

    def get_arguments(self):
        super().get_arguments()
        self._xcm_siz = self._extractor.get_value("windows_size")
        self._vie_cam_pos = self._extractor.get_value("camera_position")
        self._vie_cam_reference = self._extractor.get_value("camera_reference")
        self._vie_cam_upvector = self._extractor.get_value("camera_upvector")
        self._vie_cen = self._extractor.get_value("center_view")
        self._vie_res = self._extractor.get_value("reset_view")
        self._vie_scale = self._extractor.get_value("zoom")
        self._fn_display = self._extractor.get_value("display")
        self._view_default = self._extractor.get_value("default")
        self._view_file = self._extractor.get_value("filename")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()

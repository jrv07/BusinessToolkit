from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent


class AnimatorInstructionSetView(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._xcm_siz = None  # parameters.get('windows_size', None)  # [600, 300]
        self._vie_cam_dir = None  # parameters.get('camera_direction', None)  # (top/bot/left/rig/fro/rea)
        self._vie_camera_direction_angle = None  # parameters.get('camera_direction_angle', None)  # [0, -90, -90]
        self._vie_cen = None  # parameters.get('center_view', None)  # True/False; vie: cen / vie_cen
        self._vie_ref = None  # parameters.get('refresh_view', None)  # True/False; vie: ref / vie_ref
        self._vie_res = None  # parameters.get('reset_view', None)  # True/False; vie: res / vie_res
        self._vie_cam_pos = None  # parameters.get('camera_pos', None)  # [25000, -600, 1400]
        self._camera_clipping_plane = None  # parameters.get('camera_clipping_plane', None)  # [2747.81, 28747.8]
        self._vie_scale = None  # parameters.get('zoom', None)  # float value
        self._fn_display = None
        self._user_command = None
        self._extractor.add_list("windows_size", entry_type=int, length=2, optional=False, default=[900, 600],
                                 description="window size")
        camera_directions = ["top", "bot", "left", "rig", "fro", "rea"]
        self._extractor.add_str("camera_direction", valid_values=camera_directions,
                                description="camera direction/vector")
        self._extractor.add_list("camera_direction_angle", entry_type=int, length=3,
                                 description="camera direction/vector")
        self._extractor.add_bool("center_view", description="view centre on/off")
        self._extractor.add_bool("refresh_view", description="view refresh on/off")
        self._extractor.add_bool("reset_view", description="view reset on/off")
        self._extractor.add_list("camera_position", entry_type=float, length=3, description="camera position")
        self._extractor.add_list("camera_clipping_plane", entry_type=float, length=2, description="")
        self._extractor.add_float("zoom", description="zoom factor in/out")
        display_type = ["shm", "she", "sho", "sme", "smm", "smo", "soe", "som"]
        self._extractor.add_str("display", valid_values=display_type, default="she", description="display geo/mesh")
        self._extractor.add_list("user_command", entry_type=str, optional=True, description="user command")

    def generate_instruction(self):
        for slot in self._slots:
            if self._xcm_siz is not None:
                self.add_slot_command(slot, "xcm siz {} {}".format(str(self._xcm_siz[0]), str(self._xcm_siz[1])))

            if self._vie_cam_pos is not None:
                coord = list(map(lambda coord_entry: str(coord_entry), self._vie_cam_pos))
                self.add_slot_command(slot, "vie cam pos xyz {}".format(" ".join(coord)))

            if self._vie_cam_dir is not None:
                self.add_slot_command(slot, "vie cam dir {}".format(self._vie_cam_dir))

            if self._vie_camera_direction_angle is not None:
                vec = list(map(lambda vec_entry: str(vec_entry), self._vie_camera_direction_angle))
                self.add_slot_command(slot, "vie cam rdi {}".format(" ".join(vec)))

            if self._camera_clipping_plane is not None:
                coord = list(map(lambda coord_entry: str(coord_entry), self._camera_clipping_plane))
                self.add_slot_command(slot, "vie cam cli {}".format(" ".join(coord)))

            if self._vie_cen is not None:
                if self._vie_cen:
                    self.add_slot_command(slot, "vie cen")

            if self._vie_ref is not None:
                if self._vie_ref:
                    self.add_slot_command(slot, "vie ref")

            if self._vie_res is not None:
                if self._vie_res:
                    self.add_slot_command(slot, "vie res")

            if self._vie_scale is not None:
                self.add_slot_command(slot, "vie sca {}".format(str(self._vie_scale)))

            if self._fn_display is not None:
                self.add_slot_command(slot, "sty pid {} all".format(self._fn_display))

            if self._user_command is not None:
                for item in self._user_command:
                    self.add_slot_command(slot, "{}".format(item))

    def get_arguments(self):
        super().get_arguments()
        self._xcm_siz = self._extractor.get_value("windows_size")
        self._vie_cam_dir = self._extractor.get_value("camera_direction")
        self._vie_camera_direction_angle = self._extractor.get_value("camera_direction_angle")
        self._vie_cen = self._extractor.get_value("center_view")
        self._vie_ref = self._extractor.get_value("refresh_view")
        self._vie_res = self._extractor.get_value("reset_view")
        self._vie_cam_pos = self._extractor.get_value("camera_position")
        self._camera_clipping_plane = self._extractor.get_value("camera_clipping_plane")
        self._vie_scale = self._extractor.get_value("zoom")
        self._fn_display = self._extractor.get_value("display")
        self._user_command = self._extractor.get_value("user_command")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()


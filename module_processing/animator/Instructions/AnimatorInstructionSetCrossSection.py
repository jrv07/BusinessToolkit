from module_processing.animator.Instructions.AnimatorInstructionSlotDependent import AnimatorInstructionSlotDependent
import logging


class AnimatorInstructionSetCrossSection(AnimatorInstructionSlotDependent):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._crs_pos_tai = None  # currentCrossSection.get('base_point', None)  # [2000,0,0] # "2000 0 0"# crs pos tai
        self._crs_pos_dir = None  # currentCrossSection.get('direction', None)  # [-1,0,0] # "-1 0 0"# crs pos dir
        self._crs_pos_nod = None  # currentCrossSection.get('nodes', None)  # [123, 1245, 567] # crs pos nod/no2/no3
        self._crs_typ = None  # currentCrossSection.get('type', "lag")  # lag/eul - lagrange/euler # crs typ lag
        self._crs_geo_crs_cli = None  # currentCrossSection.get('geometry', "cut")  # hide/show/cut # crs geo & crs cli
        self._crs_lin = None  # currentCrossSection.get('line', None)  # on/off # crs lin
        self._crs_pco = None  # currentCrossSection.get('line_color', None)  # col/pid/pco # " 0 0 0.2" # col crs blue
        self._sty_crs_wid = None  # currentCrossSection.get('line_width', None)  # sty crs wid 'float'
        self._sty_crs = None  # currentCrossSection.get('line_style', None)  # con/dad/das/dot # sty crs
        self._gri = None  # currentCrossSection.get('grid', 'off')  # gri on/off  [off]
        self._crs = None  # currentCrossSection.get('crs', 'off')  # crs on/off  [off]
        self._gri_hor = None  # currentCrossSection.get('grid_horizontal', None)   # [0, 400, 100] # gri hor
        self._gri_ver = None  # currentCrossSection.get('grid_vertical', None)  # "500 2800 100" # gri ver
        self._gri_cen = None  # currentCrossSection.get('grid_center', None)  # True/False-on/off # gri cen
        self._gri_gfs = None  # currentCrossSection.get('grid_font', None)  # gri gfs 1.0 # grid font scale
        self._user_command = None
        self._extractor.add_list("base_point", entry_type=int, length=3, description="cross section position")
        self._extractor.add_list("direction", entry_type=float, length=3, description="cross section vector/direction")
        self._extractor.add_list("nodes", entry_type=int, length=3, description="")
        self._extractor.add_str("type", valid_values=["lag", "eul"], optional=True, default="lag",
                                description="cross section type")
        self._extractor.add_str("geometry", valid_values=["hide", "show", "cut"], optional=True, default="cut",
                                description="cross section geometry on/off/cut")
        self._extractor.add_bool("line", description="cross section line on/off")
        self._extractor.add_bool("line_pid_color", description="cross section color on/off")
        self._extractor.add_float("line_width", description="cross section line thickness")
        self._extractor.add_str("line_style", valid_values=["con", "dad", "das", "dot"],
                                description="cross section line style")
        self._extractor.add_bool("grid", description="cross section grid on/off")
        self._extractor.add_bool("crs", description="cross section on/off")
        self._extractor.add_list("grid_horizontal", entry_type=int, length=3, description="cross section grid x-range")
        self._extractor.add_list("grid_vertical", entry_type=int, length=3, description="cross section grid y-range")
        self._extractor.add_bool("grid_center", description="cross section grid centre on/off")
        self._extractor.add_float("grid_font_scale", description="cross section grid font size")
        self._extractor.add_list("user_command", entry_type=str, optional=True, description="user command")

    def validate(self):
        if (self._crs_pos_tai is not None or self._crs_pos_dir is not None) and self._crs_pos_nod is not None:
            logging.error("warning: base_point and direction will be overwritten by nodes.")
        elif (self._crs_pos_tai is None or self._crs_pos_dir is None) and self._crs_pos_nod is None:
            logging.error("warning: Either base_point and direction or nodes must be given.")
            # raise ValueError
        if (self._gri_hor is not None or self._gri_ver is not None) and self._gri_cen is not None:
            logging.error("warning: grid_horizontal and grid_vertical will be overwritten by grid_center.")

    def generate_instruction(self):
        self.validate()
        for slot in self._slots:
            if self._crs_pos_tai is not None:
                coord = list(map(lambda coord_entry: str(coord_entry), self._crs_pos_tai))
                self.add_slot_command(slot, "crs pos tai {}".format(" ".join(coord)))

            if self._crs_pos_dir is not None:
                coord = list(map(lambda coord_entry: str(coord_entry), self._crs_pos_dir))
                self.add_slot_command(slot, "crs pos dir {}".format(" ".join(coord)))

            if self._crs_pos_nod is not None:
                coord = list(map(lambda coord_entry: str(coord_entry), self._crs_pos_nod))
                self.add_slot_command(slot, "crs pos nod {}".format("/".join(coord)))

            if self._crs_typ is not None:
                self.add_slot_command(slot, "crs typ {}".format(self._crs_typ))

            if self._crs_geo_crs_cli is not None:
                if self._crs_geo_crs_cli == "hide":
                    self.add_slot_command(slot, "crs geo off")
                    self.add_slot_command(slot, "crs cli on")
                elif self._crs_geo_crs_cli == "show":
                    self.add_slot_command(slot, "crs geo on")
                    self.add_slot_command(slot, "crs cli off")
                elif self._crs_geo_crs_cli == "cut":
                    self.add_slot_command(slot, "crs geo on")
                    self.add_slot_command(slot, "crs cli on")

            if self._crs_lin is not None:
                self.add_slot_command(slot, "crs lin {}".format(self.get_on_off(self._crs_lin)))

            if self._crs_pco is not None:
                self.add_slot_command(slot, "crs pco {}".format(self.get_on_off(self._crs_pco)))

            if self._sty_crs_wid is not None:
                self.add_slot_command(slot, "sty crs wid {}".format(self._sty_crs_wid))

            if self._sty_crs is not None:
                self.add_slot_command(slot, "sty crs {}".format(self._sty_crs))

            if self._gri is not None:
                self.add_slot_command(slot, "gri {}".format(self.get_on_off(self._gri)))

            if self._gri_hor is not None:
                nodes = map(lambda node: str(node), self._gri_hor)
                self.add_slot_command(slot, "gri hor {}".format(" ".join(nodes)))

            if self._gri_ver is not None:
                nodes = map(lambda node: str(node), self._gri_ver)
                self.add_slot_command(slot, "gri ver {}".format(" ".join(nodes)))

            if self._gri_cen is not None:
                self.add_slot_command(slot, "gri cen {}".format(self._gri_cen))

            if self._gri_gfs is not None:
                self.add_slot_command(slot, "gri gfs {}".format(self._gri_gfs))

            if self._crs is not None:
                self.add_slot_command(slot, "crs swi {}".format(self.get_on_off(self._crs)))

            if self._user_command is not None:
                for item in self._user_command:
                    self.add_slot_command(slot, "{}".format(item))

    def get_arguments(self):
        super().get_arguments()
        self._crs_pos_tai = self._extractor.get_value("base_point")
        self._crs_pos_dir = self._extractor.get_value("direction")
        self._crs_pos_nod = self._extractor.get_value("nodes")
        self._crs_typ = self._extractor.get_value("type")
        self._crs_geo_crs_cli = self._extractor.get_value("geometry")
        self._crs_lin = self._extractor.get_value("line")
        self._crs_pco = self._extractor.get_value("line_pid_color")
        self._sty_crs_wid = self._extractor.get_value("line_width")
        self._sty_crs = self._extractor.get_value("line_style")
        self._gri = self._extractor.get_value("grid")
        self._crs = self._extractor.get_value("crs")
        self._gri_hor = self._extractor.get_value("grid_horizontal")
        self._gri_ver = self._extractor.get_value("grid_vertical")
        self._gri_cen = self._extractor.get_value("grid_center")
        self._gri_gfs = self._extractor.get_value("grid_font_scale")
        self._user_command = self._extractor.get_value("user_command")

    def generate(self):
        self.extract()
        self.get_arguments()
        if not self.check_source():
            super().generate()
            self.generate_instruction()
            self.generate_store_data()


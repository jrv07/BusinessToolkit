from module_misc.BasicTask import BasicTask
from pptx.dml.color import RGBColor
import logging


class PptxColor(BasicTask):
    def __init__(self, parameters=None):
        super().__init__(parameters)
        self._color = None
        self._color_input = None
        self._color_input_type = None
        self._extractor.add_list("rgb_list", specifier="rgb", entry_type=int, length=3, optional=False,
                                 alternative="rgb_str",
                                 description="specify the RGB values as list of integers from 0 to 255. "
                                             "Example: [10, 0, 240].")
        self._extractor.add_str("rgb_str", specifier="rgb", optional=False, alternative="hex",
                                description="specify the RGB values as string with three space separated rgb values."
                                            "Example: '10 0 240'.")
        self._extractor.add_str("hex", specifier="hex", optional=False,
                                description="specify the color in hex format."
                                            "Example: 'FFFFFF' for white color.")
        self._extractor.set_group_name("Presentation")

    @property
    def value(self):
        return self._color

    @staticmethod
    def generate_color_from_rgb_list(rgb_list):
        if len(rgb_list) != 3:
            logging.error("Not exactly 3 values for rgb color specified")
            raise ValueError
        try:
            r = int(rgb_list[0])
            g = int(rgb_list[1])
            b = int(rgb_list[2])
        except Exception:
            logging.error("The rgb values must be of type integer and each between 0 and 255.")
            raise ValueError
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return RGBColor(r, g, b)
        else:
            logging.error("The rgb values are not between 0 and 255.")
            raise ValueError

    def generate_color(self):
        if self._color_input_type == "rgb_list":
            rgb_list = [self._color_input[0], self._color_input[1], self._color_input[2]]
            self._color = self.generate_color_from_rgb_list(rgb_list)
        elif self._color_input_type == "rgb_str":
            rgb_list = self._color_input.split(" ")
            self._color = self.generate_color_from_rgb_list(rgb_list)
        elif self._color_input_type == "hex":
            self._color = RGBColor.from_string(self._color_input)

    def get_arguments(self):
        super().get_arguments()
        self._color_input = self._extractor.get_value("rgb_str")
        if self._color_input is None:
            self._color_input = self._extractor.get_value("rgb_list")
            if self._color_input is None:
                self._color_input = self._extractor.get_value("hex")
                self._color_input_type = "hex"
            else:
                self._color_input_type = "rgb_list"
        else:
            self._color_input_type = "rgb_str"

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_color()

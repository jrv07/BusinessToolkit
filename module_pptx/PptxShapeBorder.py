from module_misc.BasicTask import BasicTask
from module_pptx.pptx_styles.PptxColor import PptxColor


class PptxShapeBorder(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._border_width = None
        self._border_color_input = None
        self._border_color: PptxColor = None
        self._extractor.add_int("width", optional=False, description="")
        self._extractor.add_object("color", object_type=PptxColor, description="")
        self._extractor.set_group_name("Presentation")

    @property
    def width(self):
        return self._border_width

    @property
    def color(self):
        return self._border_color

    def generate_border_color(self):
        if self._border_color_input is not None:
            self._border_color = PptxColor(self._border_color_input)
            self._border_color.generate()

    def get_arguments(self):
        super().get_arguments()
        self._border_width = self._extractor.get_value("width")
        self._border_color_input = self._extractor.get_value("color")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_border_color()

from module_misc.BasicTask import BasicTask
from module_pptx.PptxShapeBorder import PptxShapeBorder
from pptx.util import Cm, Pt
from pptx.slide import Slide


class PptxShape(BasicTask):
    def __init__(self, parameters, slide, settings):
        super().__init__(parameters, settings)
        self._slide: Slide = slide
        self._height: Cm = None
        self._width: Cm = None
        self._left = Cm(0)
        self._top = Cm(0)
        self._shape_object = None
        self._position_input = None
        self._size_input = None
        self._extractor.add_list("position", entry_type=float, length=2, description="")
        self._extractor.add_list("size", entry_type=float, length=2, description="")

    def get_arguments(self):
        super().get_arguments()
        self._position_input = self._extractor.get_value("position")
        self._size_input = self._extractor.get_value("size")

    def generate_position(self):
        if self._position_input is not None:
            self._left = Cm(self._position_input[0])
            self._top = Cm(self._position_input[1])

    def generate_size(self):
        if self._size_input is not None:
            self._height = Cm(self._size_input[0])
            self._width = Cm(self._size_input[1])

    def generate(self):
        self.generate_position()
        self.generate_size()


class PptxShapeWithBorder(PptxShape):
    def __init__(self, parameters, slide, settings):
        super().__init__(parameters, slide, settings)
        self._border_input = None
        self._border: PptxShapeBorder = None
        self._extractor.add_object("border", PptxShapeBorder, description="")

    def apply_styles(self):
        if self._border is not None:
            line = self._shape_object.line
            line.color.rgb = self._border.color.value
            line.width = Pt(self._border.width)

    def get_arguments(self):
        super().get_arguments()
        self._border_input = self._extractor.get_value("border")

    def generate_border(self):
        if self._border_input is not None:
            border = PptxShapeBorder(self._border_input)
            border.generate()
            self._border = border

    def generate(self):
        super().generate()
        self.generate_border()

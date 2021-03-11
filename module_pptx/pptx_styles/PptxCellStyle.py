from pptx.util import Cm
from pptx.table import _Cell
from pptx.enum.text import MSO_VERTICAL_ANCHOR as MSO_ANCHOR
from module_pptx.pptx_styles.PptxStyle import PptxStyle
from module_pptx.pptx_styles.PptxColor import PptxColor


class PptxCellStyle(PptxStyle):
    def __init__(self, parameters=None):
        super().__init__(parameters)
        self._width: Cm = None
        self._height: Cm = None
        self._vertical_anchor = None
        self._vertical_anchor_input = None
        self._fill_color: PptxColor = None
        self._fill_color_input = None
        self._rotated = None
        self._extractor.add_float("width", description="")
        self._extractor.add_list("size", entry_type=float, length=2, description="")
        self._extractor.add_object("fill_color", object_type=PptxColor, description="")
        valid_vertical_anchors = ["middle", "top", "bottom"]
        self._extractor.add_str("vertical_anchor", valid_values=valid_vertical_anchors, description="")
        self._extractor.add_bool("rotated", description="")
        self._extractor.set_group_name("Presentation")

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def vertical_anchor(self):
        return self._vertical_anchor

    @property
    def fill_color(self):
        return self._fill_color

    @property
    def rotated(self):
        return self._rotated

    def update_styles_by_object(self, styles_object: "PptxCellStyle"):
        if styles_object.width is not None:
            self._width = styles_object.width
        if styles_object.height is not None:
            self._height = styles_object.height
        if styles_object.vertical_anchor is not None:
            self._vertical_anchor = styles_object.vertical_anchor
        if styles_object.fill_color is not None:
            self._fill_color = styles_object.fill_color
        if styles_object.rotated is not None:
            self._rotated = styles_object.rotated

    def apply_styles(self, cell: _Cell):
        if self._fill_color is not None:
            cell.fill.solid()
            cell.fill.fore_color.rgb = self._fill_color.value
        if self._vertical_anchor is not None:
            cell.vertical_anchor = self._vertical_anchor
        if self._rotated is not None:
            tcpr = cell._tc.get_or_add_tcPr()
            tcpr.set('vert', 'vert270')

    def generate_fill_color(self):
        if self._fill_color_input is not None:
            self._fill_color = PptxColor(self._fill_color_input)
            self._fill_color.generate()

    def generate_vertical_anchor(self):
        if self._vertical_anchor_input is not None:
            if self._vertical_anchor_input == "middle":
                self._vertical_anchor = MSO_ANCHOR.MIDDLE
            elif self._vertical_anchor_input == "top":
                self._vertical_anchor = MSO_ANCHOR.TOP
            elif self._vertical_anchor_input == "bottom":
                self._vertical_anchor = MSO_ANCHOR.BOTTOM

    def get_arguments(self):
        super().get_arguments()
        width = self._extractor.get_value("width")
        if width is not None:
            self._width = Cm(width)
        size = self._extractor.get_value("size")
        if size is not None:
            self._width = Cm(size[0])
            self._height = Cm(size[1])
        self._fill_color_input = self._extractor.get_value("fill_color")
        self._vertical_anchor_input = self._extractor.get_value("vertical_anchor")
        self._rotated = self._extractor.get_value("rotated")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_vertical_anchor()
        self.generate_fill_color()

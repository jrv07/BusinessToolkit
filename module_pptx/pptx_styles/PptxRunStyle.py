from pptx.util import Pt
from pptx.text.text import _Run
from pptx.enum.text import MSO_TEXT_UNDERLINE_TYPE
from module_pptx.pptx_styles.PptxStyle import PptxStyle
from module_pptx.pptx_styles.PptxColor import PptxColor


class PptxRunStyle(PptxStyle):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._font_color: PptxColor = None
        self._font_color_input = None
        self._font_size = None
        self._font_bold = None
        self._font_italic = None
        self._font_underline = None
        self._font_name = None
        self._extractor.add_object("font_color", object_type=PptxColor, description="")
        self._extractor.add_int("font_size", description="")
        self._extractor.add_bool("font_bold", description="")
        self._extractor.add_bool("font_italic", description="")
        self._extractor.add_str("font_name", description="")
        self._extractor.add_bool("font_underline", description="")
        self._extractor.set_group_name("Presentation")

    @property
    def font_color(self):
        return self._font_color

    @property
    def font_size(self):
        return self._font_size

    @property
    def font_bold(self):
        return self._font_bold

    @property
    def font_italic(self):
        return self._font_italic

    @property
    def font_name(self):
        return self._font_name

    @property
    def font_underline(self):
        return self._font_underline

    def update_styles_by_object(self, styles_object: "PptxRunStyle"):
        if styles_object.font_color is not None:
            self._font_color = styles_object.font_color
        if styles_object.font_size is not None:
            self._font_size = styles_object.font_size
        if styles_object.font_bold is not None:
            self._font_bold = styles_object.font_bold
        if styles_object.font_italic is not None:
            self._font_italic = styles_object.font_italic
        if styles_object.font_name is not None:
            self._font_name = styles_object.font_name
        if styles_object.font_underline is not None:
            self._font_underline = styles_object.font_underline

    def apply_styles(self, run: _Run):
        if self._font_size is not None:
            run.font.size = self._font_size
        if self._font_bold is not None:
            run.font.bold = self._font_bold
        if self._font_italic is not None:
            run.font.italic = self._font_italic
        if self._font_underline is not None:
            if self._font_underline:
                run.font.underline = MSO_TEXT_UNDERLINE_TYPE.SINGLE_LINE
        if self._font_color is not None:
            run.font.color.rgb = self._font_color.value
        if self._font_name is not None:
            run.font.name = self._font_name

    def generate_font_color(self):
        if self._font_color_input is not None:
            self._font_color = PptxColor(self._font_color_input)
            self._font_color.generate()

    def get_arguments(self):
        super().get_arguments()
        self._font_color_input = self._extractor.get_value("font_color")
        font_size = self._extractor.get_value("font_size")
        if font_size is not None:
            self._font_size = Pt(font_size)
        self._font_bold = self._extractor.get_value("font_bold")
        self._font_italic = self._extractor.get_value("font_italic")
        self._font_name = self._extractor.get_value("font_name")
        self._font_underline = self._extractor.get_value("font_underline")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_font_color()

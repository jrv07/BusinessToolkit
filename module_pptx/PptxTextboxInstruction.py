from module_pptx.PptxShapes import PptxShapeWithBorder
from module_pptx.PptxTextContent import PptxTextContent
from module_pptx.PptxTextContentEntry import PptxTextContentEntry
from module_pptx.pptx_styles.PptxParagraphStyle import PptxParagraphStyle


class PptxTextboxInstruction(PptxShapeWithBorder):
    def __init__(self, parameters, slide, settings=None):
        super().__init__(parameters, slide, settings)
        self._placeholder = None
        self._contents_input = None
        self._default_style_input = None
        self._extractor.add_object("style", PptxParagraphStyle, description="")
        self._extractor.add_list("content_multi", specifier="content", entry_type=dict,
                                 entry_object_type=PptxTextContentEntry, optional=False, alternative="content_single",
                                 description="")
        self._extractor.add_object("content_single", PptxTextContentEntry, specifier="content", optional=False,
                                   description="")
        self._extractor.add_int("placeholder", description="")
        self._extractor.set_group_name("Presentation")
        self._text_frame = None
        self._contents = []
        # self._paragraph = None
        # self._runs = []

    # def extract_placeholder(self):
    #     self._placeholder = extract_value_int("placeholder", self._parameters)
    #
    # def extract_content(self):
    #     self._content_input = extract_value_list("content", self._parameters, entry_type=dict, optional=False)
    #
    # def extract_style(self):
    #     self._default_style_input = get_dict_value("style", self._parameters)

    def get_shape_object(self):
        if self._placeholder is not None:
            shape_object = self._slide.placeholders[self._placeholder]
        else:
            shape_object = self._slide.shapes.add_textbox(self._left, self._top, self._height, self._width)
        self._text_frame = shape_object.text_frame

    def generate_textbox(self):
        self.apply_styles()
        text_content = PptxTextContent(self._contents_input, self._default_style_input, self._text_frame)
        text_content.apply_styles()

    def get_arguments(self):
        super().get_arguments()
        self._contents_input = self._extractor.get_value("content_multi")
        if self._contents_input is None:
            self._contents_input = [self._extractor.get_value("content_single")]
        self._placeholder = self._extractor.get_value("placeholder")
        self._default_style_input = self._extractor.get_value("style")

    def generate(self):
        self.extract()
        self.get_arguments()
        # self.extract_placeholder()
        # self.extract_content()
        # self.extract_style()
        super().generate()
        self.get_shape_object()
        self.generate_textbox()

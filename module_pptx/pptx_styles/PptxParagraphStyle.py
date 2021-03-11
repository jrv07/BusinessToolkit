from pptx.text.text import _Paragraph
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from module_pptx.pptx_styles.PptxStyle import PptxStyle


class PptxParagraphStyle(PptxStyle):
    def __init__(self, parameters=None):
        super().__init__(parameters)
        self._alignment_input = None
        self._extractor.add_str("alignment", description="")
        self._extractor.set_group_name("Presentation")
        self._alignment = None

    @property
    def alignment(self):
        return self._alignment

    def update_styles_by_object(self, styles_object: "PptxParagraphStyle"):
        if styles_object.alignment is not None:
            self._alignment = styles_object.alignment

    def generate_alignment(self):
        if self._alignment_input is not None:
            if self._alignment_input == "center":
                self._alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
            elif self._alignment_input == "left":
                self._alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
            elif self._alignment_input == "right":
                self._alignment = PP_PARAGRAPH_ALIGNMENT.RIGHT

    def apply_styles(self, paragraph: _Paragraph):
        if self._alignment is not None:
            paragraph.alignment = self._alignment

    def get_arguments(self):
        super().get_arguments()
        self._alignment_input = self._extractor.get_value("alignment")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_alignment()

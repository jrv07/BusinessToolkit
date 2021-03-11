from pptx.text.text import TextFrame
from module_pptx.pptx_styles.PptxStyle import PptxStyle


class PptxTextFrameStyle(PptxStyle):
    def __init__(self, parameters=None):
        super().__init__(parameters)
        self._word_wrap = None
        self._extractor.add_bool("word_wrap", description="")
        self._extractor.set_group_name("Presentation")

    @property
    def word_wrap(self):
        return self._word_wrap

    def update_styles_by_object(self, styles_object: "PptxTextFrameStyle"):
        if styles_object.word_wrap is not None:
            self._word_wrap = styles_object.word_wrap

    # def extract_word_wrap(self):
    #     self._word_wrap = extract_value_bool("word_wrap", self._parameters)

    def apply_styles(self, text_frame: TextFrame):
        if self._word_wrap is not None:
            text_frame.word_wrap = self._word_wrap

    def get_arguments(self):
        super().get_arguments()
        self._word_wrap = self._extractor.get_value("word_wrap")

    def generate(self):
        self.extract()
        self.get_arguments()
        # if self._parameters is not None:
        #     self.extract_word_wrap()

from pptx.text.text import _Run
from module_misc.BasicTask import BasicTask
from module_pptx.pptx_styles.PptxRunStyle import PptxRunStyle
from module_pptx.PptxFromVariable import PptxFromVariable


class PptxTextContentEntry(BasicTask):
    def __init__(self, parameters, default_styles, run):
        super().__init__(parameters)
        self._default_styles = default_styles
        self._text = None
        self._font_input = None
        self._run: _Run = run
        self._extractor.add_str("text_str", specifier="text", optional=False, alternative="text_float", description="")
        self._extractor.add_float("text_float", specifier="text", optional=False, alternative="from_variable", description="")
        self._extractor.add_object("from_variable", optional=False, object_type=PptxFromVariable, description="")
        self._extractor.add_object("font", PptxRunStyle, description="")
        self._extractor.set_group_name("Presentation")

    def get_arguments(self):
        super().get_arguments()
        self._text = self._extractor.get_value("text_str")
        if self._text is None:
            text = self._extractor.get_value("text_float")
            if text is not None:
                self._text = str(text)
        if self._text is None:
            from_variable_input = self._extractor.get_value("from_variable")
            from_variable = PptxFromVariable(from_variable_input)
            from_variable.generate()
            self._text = from_variable.value
        if self._text == "":
            self._text = " "
        self._font_input = self._extractor.get_value("font")

    def apply_text(self):
        self._run.text = self._text
        run_style = PptxRunStyle(self._default_styles)
        run_style.update_styles_by_input(self._font_input)
        run_style.generate()
        run_style.apply_styles(self._run)

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.apply_text()

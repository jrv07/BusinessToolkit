from module_pptx.PptxPage import PptxPage
from module_pptx.PptxTextboxInstruction import PptxTextboxInstruction


class PptxTitlePage(PptxPage):
    def __init__(self, parameters, presentation, settings=None):
        super().__init__(parameters, presentation, 0, settings)
        self._topic = None
        self._extractor.add_str("topic", optional=False, description="")
        self._extractor.set_group_name("Presentation")

    def generate_title_text(self):
        instruction_input = {
            "placeholder": 10,
            "content": {
                "text": self._topic
            }
        }
        instruction = PptxTextboxInstruction(instruction_input, self._slide, self._settings)
        instruction.generate()
        self._instructions.append(instruction)

    def get_arguments(self):
        super().get_arguments()
        self._topic = self._extractor.get_value("topic")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_title_text()

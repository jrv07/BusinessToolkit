from module_pptx.PptxPage import PptxPage
from module_pptx.PptxInstructionFactory import PptxInstructionFactory


class PptxContentPage(PptxPage):
    def __init__(self, parameters, presentation, settings=None):
        super().__init__(parameters, presentation, 1, settings)
        self._extractor.add_list("instructions", entry_type=dict, entry_object_type=PptxInstructionFactory,
                                 optional=False, description="instruction")
        self._extractor.set_group_name("Presentation")

    def get_arguments(self):
        super().get_arguments()
        self._instructions_input = self._extractor.get_value("instructions")

    def generate_instructions(self):
        for instruction_input in self._instructions_input:
            instruction = PptxInstructionFactory(self._slide, instruction_input, self._settings)
            instruction.generate()
            self._instructions.append(instruction)

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_instructions()

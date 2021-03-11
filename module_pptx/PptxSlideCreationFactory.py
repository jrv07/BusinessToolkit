from module_misc.InstructionFactory import InstructionFactory
from module_pptx.PptxContentPage import PptxContentPage
from module_pptx.PptxTitlePage import PptxTitlePage
from module_pptx.PptxContactPage import PptxContactPage
from module_pptx.PptxPage import PptxPage


class PptxSlideCreationFactory(InstructionFactory):
    def __init__(self, parameters, presentation, settings=None):
        super().__init__(parameters, PptxPage, [presentation])
        self._slide_instruction_name = None
        self._slide_instruction_input = None
        self._slide_instruction = None
        self._extractor.add_object("title_page", PptxTitlePage, description="")
        self._extractor.add_object("contact_page", PptxContactPage, description="")
        self._extractor.add_object("page", PptxContentPage, description="")
        self._extractor.set_name("PptxSlide")
        self._extractor.set_group_name("Presentation")

    def generate(self):
        super().generate()
        self.generate_instruction()

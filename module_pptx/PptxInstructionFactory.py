from module_pptx.PptxTextboxInstruction import PptxTextboxInstruction
from module_pptx.PptxPictureInstruction import PptxPictureInstruction
from module_pptx.PptxMovieInstruction import PptxMovieInstruction
from module_pptx.PptxTableManualInstruction import PptxTableManualInstruction
from module_pptx.PptxTableFromDataInstruction import PptxTableFromDataInstruction
from module_misc.InstructionFactory import InstructionFactory
from module_pptx.PptxShapes import PptxShape


class PptxInstructionFactory(InstructionFactory):
    def __init__(self, slide, parameters, settings=None):
        super().__init__(parameters, PptxShape, [slide])
        self._extractor.add_object("text", PptxTextboxInstruction, description="")
        self._extractor.add_object("picture", PptxPictureInstruction, description="")
        self._extractor.add_object("movie", PptxMovieInstruction, description="")
        self._extractor.add_object("table_manual", PptxTableManualInstruction, description="")
        self._extractor.add_object("table_from_data", PptxTableFromDataInstruction, description="")
        self._extractor.set_name("PptxInstruction")
        self._extractor.set_group_name("Presentation")

    def generate(self):
        super().generate()
        self.generate_instruction()

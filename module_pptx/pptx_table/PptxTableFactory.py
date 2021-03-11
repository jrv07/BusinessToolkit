from module_misc.InstructionFactory import InstructionFactory
from module_pptx.pptx_table.PptxTableBase import PptxTableBase
from module_pptx.PptxTableFromDataInstruction import PptxTableFromDataInstruction
from module_pptx.PptxTableManualInstruction import PptxTableManualInstruction


class PptxTableFactory(InstructionFactory):
    def __init__(self, parameters):
        super().__init__(parameters, PptxTableBase)
        self._extractor.add_object("table_manual", PptxTableManualInstruction, description="")
        self._extractor.add_object("table_from_data", PptxTableFromDataInstruction, description="")
        self._extractor.set_name("PptxTable")
        self._extractor.set_group_name("Presentation")

    def generate(self):
        super().generate()
        self.generate_instruction()

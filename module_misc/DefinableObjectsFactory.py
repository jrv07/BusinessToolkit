from module_misc.InstructionFactory import InstructionFactory
from module_pptx.pptx_table.PptxTableStyleDefinitions import PptxTableStyleDefinitions
from module_misc.BasicTask import BasicTask


class DefinableObjectsFactory(InstructionFactory):
    def __init__(self, parameters):
        super().__init__(parameters, BasicTask)
        self._extractor.add_object("table_style_definitions", PptxTableStyleDefinitions, description="")
        self._extractor.set_name("DefinableObject")
        self._extractor.set_group_name("Misc")

    def generate(self):
        super().generate()
        self.generate_instruction()

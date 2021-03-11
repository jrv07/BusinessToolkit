from module_pptx.pptx_table.PptxTableTextCell import PptxTableTextCell
from module_pptx.pptx_table.PptxTableThresholdsCell import PptxTableThresholdsCell
from module_pptx.pptx_table.PptxTableValueCell import PptxTableValueCell
from module_pptx.pptx_table.PptxTableCellBase import PptxTableCellBase
from module_misc.InstructionFactory import InstructionFactory


class PptxTableCellFactory(InstructionFactory):
    def __init__(self, parameters, default_cell_style=None):
        super().__init__(parameters, PptxTableCellBase, [default_cell_style])
        self._extractor.add_object("text_cell", PptxTableTextCell,
                                   description="text cell with possibility of formatting the value")
        self._extractor.add_object("thresholds_cell", PptxTableThresholdsCell,
                                   description="different formats depending on the value")
        self._extractor.add_object("value_cell", PptxTableValueCell,
                                   description="value cell with possibility of formatting the value")
        self._extractor.set_name("PptxTableCell")
        self._extractor.set_group_name("Presentation")

    def generate(self):
        super().generate()
        self.generate_instruction()

from pptx.util import Cm
from typing import List
from module_pptx.pptx_table.PptxTableCellFactory import PptxTableCellFactory
from module_pptx.pptx_table.PptxTableCellBase import PptxTableCellBase
from module_misc.BasicTask import BasicTask


class PptxTableRow(BasicTask):
    def __init__(self, parameters, col_count=0, cell_default_style=None):
        super().__init__(parameters)
        self._col_count = col_count
        self._cell_default_style = cell_default_style
        self._height_input = None
        self._cells_input = None
        self._extractor.add_list("cells", optional=False, entry_type=dict, entry_object_type=PptxTableCellFactory,
                                 length=col_count, description="")
        self._extractor.add_float("height", description="")
        self._row_cells: List[PptxTableCellBase] = []
        self._row_height = Cm(0)
        self._extractor.set_group_name("Presentation")

    @property
    def height(self):
        return self._row_height

    @height.setter
    def height(self, value):
        self._row_height = Cm(value)

    def add_row_cell(self, table_cell: PptxTableCellBase):
        self._row_cells.append(table_cell)
        self._col_count = self._col_count + 1

    def generate_row(self):
        row_cells = []
        for row_item in self._cells_input:
            table_cell = PptxTableCellFactory(row_item, self._cell_default_style)
            table_cell.generate()
            row_cells.append(table_cell.instruction)
        self._row_cells = row_cells

    def generate_height(self):
        if self._height_input is not None:
            self._row_height = Cm(self._height_input)

    def get_arguments(self):
        super().get_arguments()
        self._cells_input = self._extractor.get_value("cells")
        self._height_input = self._extractor.get_value("height")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_height()
        self.generate_row()

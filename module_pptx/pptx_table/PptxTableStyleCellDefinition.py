from module_pptx.pptx_table.PptxTableRangeDefinition import PptxTableRangeDefinition
from module_pptx.pptx_table.PptxTableCellFactory import PptxTableCellFactory
from module_misc.BasicTask import BasicTask


class PptxTableStyleCellDefinition(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._col_range_input = None
        self._row_range_input = None
        self._cell_type = None
        self._extractor.add_object("cell_type", PptxTableCellFactory, optional=False, description="")
        self._extractor.add_str("col", optional=False, description="range definition: '1' => col 1, '1:4' => cols 1-4, "
                                                                   "'3:' => cols 3 to last col")
        self._extractor.add_str("row", optional=False, description="range definition: '1' => row 1, '1:4' => rows 1-4, "
                                                                   "'3:' => rows 3 to last row")
        self._row_range: PptxTableRangeDefinition = None
        self._col_range: PptxTableRangeDefinition = None
        self._extractor.set_group_name("Presentation")

    def get_cell_type(self, row_ind: int, col_ind: int):
        if self._row_range.is_in_expression(row_ind) and self._col_range.is_in_expression(col_ind):
            return self._cell_type

    def generate_row_range(self):
        self._row_range = PptxTableRangeDefinition(self._row_range_input)

    def generate_col_range(self):
        self._col_range = PptxTableRangeDefinition(self._col_range_input)

    def get_arguments(self):
        self._col_range_input = self._extractor.get_value("col")
        self._row_range_input = self._extractor.get_value("row")
        self._cell_type = self._extractor.get_value("cell_type")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_col_range()
        self.generate_row_range()

from module_pptx.pptx_table.PptxTableRangeDefinition import PptxTableRangeDefinition
from module_misc.BasicTask import BasicTask


class PptxTableStyleColumnDefinition(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._width = None
        self._col_range_input = None
        self._extractor.add_float("width", optional=False, description="")
        self._extractor.add_str("col", optional=False, description="range definition: '1' => col 1, '1:4' => col 1-4, "
                                                                   "'3:' => cols 3 to last col")
        self._col_range: PptxTableRangeDefinition = None
        self._extractor.set_group_name("Presentation")

    def get_width(self, col_ind: int):
        if self._col_range.is_in_expression(col_ind):
            return self._width

    def generate_col_range(self):
        self._col_range = PptxTableRangeDefinition(self._col_range_input)

    def get_arguments(self):
        self._width = self._extractor.get_value("width")
        self._col_range_input = self._extractor.get_value("col")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_col_range()

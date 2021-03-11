from module_pptx.pptx_table.PptxTableRangeDefinition import PptxTableRangeDefinition
from module_misc.BasicTask import BasicTask


class PptxTableStyleRowDefinition(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._height = None
        self._row_range_input = None
        self._extractor.add_float("height", optional=False, description="")
        self._extractor.add_str("row", optional=False, description="range definition: '1' => row 1, '1:4' => rows 1-4, "
                                                                   "'3:' => rows 3 to last row")
        self._row_range: PptxTableRangeDefinition = None
        self._extractor.set_group_name("Presentation")

    def get_height(self, row_ind: int):
        if self._row_range.is_in_expression(row_ind):
            return self._height

    def generate_row_range(self):
        self._row_range = PptxTableRangeDefinition(self._row_range_input)

    def get_arguments(self):
        super().get_arguments()
        self._height = self._extractor.get_value("height")
        self._row_range_input = self._extractor.get_value("row")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_row_range()

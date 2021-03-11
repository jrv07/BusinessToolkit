from module_pptx.pptx_table.PptxTableBase import PptxTableBase
from module_pptx.pptx_styles.PptxCellStyle import PptxCellStyle
from module_pptx.pptx_table.PptxTableRow import PptxTableRow


class PptxTableManualInstruction(PptxTableBase):
    def __init__(self, parameters, slide, settings=None):
        super().__init__(parameters, slide, settings)
        self._default_cell_style = None
        self._column_widths_input = None
        self._grid_dimensions = None
        self._table_rows_input = None
        self._extractor.add_object("default_cell_style", PptxCellStyle, description="")
        self._extractor.add_list("column_widths",  optional=False, entry_type=float, description="")
        self._extractor.add_list("table_rows_columns", optional=False, entry_type=int, length=2, description="")
        self._extractor.add_list("table_rows", entry_type=dict, entry_object_type=PptxTableRow, optional=False,
                                 description="")
        self._extractor.set_group_name("Presentation")

    def generate_column_widths(self):
        self._column_widths = self.get_cm_list(self._column_widths_input)

    def generate_rows_and_cols(self):
        self._row_count = self._grid_dimensions[0]
        self._col_count = self._grid_dimensions[1]

    def generate_rows(self):
        rows = []
        for table_row_input in self._table_rows_input:
            table_row = PptxTableRow(table_row_input, self._col_count, self._default_cell_style)
            table_row.generate()
            rows.append(table_row)
        self._rows = rows

    def get_arguments(self):
        super().get_arguments()
        self._default_cell_style = self._extractor.get_value("default_cell_style")
        self._column_widths_input = self._extractor.get_value("column_widths")
        self._grid_dimensions = self._extractor.get_value("table_rows_columns")
        self._table_rows_input = self._extractor.get_value("table_rows")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_column_widths()
        self.generate_rows_and_cols()
        self.generate_rows()
        super().generate()
        self.generate_table()

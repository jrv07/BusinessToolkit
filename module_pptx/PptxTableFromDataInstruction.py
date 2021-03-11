from module_pptx.pptx_table.PptxTableBase import PptxTableBase
from module_pptx.pptx_table.PptxTableCellFactory import PptxTableCellFactory
from module_pptx.pptx_table.PptxTableRow import PptxTableRow
from module_pptx.pptx_table.PptxTableStyleDefinitions import PptxTableStyleDefinitions
from pptx.util import Cm
import numpy


class PptxTableFromDataInstruction(PptxTableBase):
    def __init__(self, parameters, slide, settings=None):
        super().__init__(parameters, slide, settings)
        self._table_content = None
        self._style_definitions_input = None
        self._transpose = None
        self._style_definitions_source: PptxTableStyleDefinitions = None
        self._style_definitions: PptxTableStyleDefinitions = None
        self._extractor.add_source("style_source", specifier="style", source_type=PptxTableStyleDefinitions, optional=False,
                                   alternative="style_defs", description="")
        self._extractor.add_object("style_defs", PptxTableStyleDefinitions, specifier="style", optional=False)
        self._extractor.add_source("content", source_type=list, optional=False, description="")
        self._extractor.add_bool("transpose", default=False, description="makes rows to cols if set to True")
        self._extractor.set_group_name("Presentation")

    def generate_styles(self):
        if self._style_definitions_source is not None:
            self._style_definitions = self._style_definitions_source
        else:
            self._style_definitions = PptxTableStyleDefinitions(self._style_definitions_input)
            self._style_definitions.generate()

    def generate_cell(self, cell_data, row_ind: int, col_ind: int):
        cell_definitions = self._style_definitions.get_cell_definitions(row_ind, col_ind)
        general_cell = PptxTableCellFactory(cell_definitions)
        general_cell.generate()
        general_cell.instruction.set_cell_value(cell_data)
        return general_cell

    def generate_column_widths(self):
        self._col_count = len(self._table_content[0])
        for col_ind in range(self._col_count):
            column_width = self._style_definitions.get_column_width(col_ind)
            self._column_widths.append(Cm(column_width))

    def generate_rows(self):
        row_ind = -1
        for data_row in self._table_content:
            col_ind = -1
            row_ind = row_ind + 1
            row_height = self._style_definitions.get_row_height(row_ind)
            row = PptxTableRow({})
            row.height = row_height
            for cell_data in data_row:
                col_ind = col_ind + 1
                general_cell = self.generate_cell(cell_data, row_ind, col_ind)
                row.add_row_cell(general_cell.instruction)
            self._rows.append(row)
            self._row_count = self._row_count + 1

    def generate_transpose(self):
        if self._transpose:
            table_content_transposed = self._table_content.transpose()
            self._table_content = table_content_transposed

    def get_arguments(self):
        super().get_arguments()
        self._table_content = numpy.array(self._extractor.get_value("content"))
        self._style_definitions_source = self._extractor.get_value("style_source")
        self._style_definitions_input = self._extractor.get_value("style_defs")
        self._transpose = self._extractor.get_value("transpose")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_transpose()
        self.generate_styles()
        self.generate_column_widths()
        self.generate_rows()
        super().generate()
        self.generate_table()

from typing import List
import logging
from module_pptx.pptx_table.PptxTableStyleRowDefinition import PptxTableStyleRowDefinition
from module_pptx.pptx_table.PptxTableStyleColumnDefinition import PptxTableStyleColumnDefinition
from module_pptx.pptx_table.PptxTableStyleCellDefinition import PptxTableStyleCellDefinition
from module_misc.BasicTask import BasicTask


class PptxTableStyleDefinitions(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._column_definitions_input = None
        self._row_definitions_input = None
        self._cell_definitions_input = None
        self._extractor.add_list("column_defs", entry_type=dict, entry_object_type=PptxTableStyleColumnDefinition, optional=False)
        self._extractor.add_list("row_defs", entry_type=dict, entry_object_type=PptxTableStyleRowDefinition, optional=False)
        self._extractor.add_list("cell_defs", entry_type=dict, entry_object_type=PptxTableStyleCellDefinition, optional=False)
        self._row_definitions: List[PptxTableStyleRowDefinition] = []
        self._column_definitions: List[PptxTableStyleColumnDefinition] = []
        self._cell_definitions: List[PptxTableStyleCellDefinition] = []
        self._extractor.set_group_name("Presentation")

    @staticmethod
    def generate_specific_definitions(definitions_input, definition_type) -> list:
        definitions = []
        if definitions_input is not None:
            for entry in definitions_input:
                range_def = definition_type(entry)
                range_def.generate()
                definitions.append(range_def)
        return definitions

    def generate_definitions(self):
        self._row_definitions = self.generate_specific_definitions(self._row_definitions_input,
                                                                   PptxTableStyleRowDefinition)
        self._column_definitions = self.generate_specific_definitions(self._column_definitions_input,
                                                                      PptxTableStyleColumnDefinition)
        self._cell_definitions = self.generate_specific_definitions(self._cell_definitions_input,
                                                                    PptxTableStyleCellDefinition)

    def get_row_height(self, row_ind: int):
        for row_def in self._row_definitions:
            height = row_def.get_height(row_ind)
            if height is not None:
                return height
        logging.error("Not all rows are matched by row definitions!")
        raise ValueError

    def get_column_width(self, col_ind: int):
        for col_def in self._column_definitions:
            width = col_def.get_width(col_ind)
            if width is not None:
                return width
        logging.error("Not all columns are matched by column definitions!")
        raise ValueError

    def get_cell_definitions(self, row_ind: int, col_ind: int):
        for cell_def in self._cell_definitions:
            cell_type = cell_def.get_cell_type(row_ind, col_ind)
            if cell_type is not None:
                return cell_type
        logging.error("Not all cells are matched by cell definitions!")
        raise ValueError

    def get_arguments(self):
        super().get_arguments()
        self._column_definitions_input = self._extractor.get_value("column_defs")
        self._row_definitions_input = self._extractor.get_value("row_defs")
        self._cell_definitions_input = self._extractor.get_value("cell_defs")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_definitions()

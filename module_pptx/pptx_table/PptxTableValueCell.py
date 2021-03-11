from pptx.table import _Cell
from module_pptx.pptx_styles.PptxCellStyle import PptxCellStyle
from module_pptx.PptxTextContent import PptxTextContent
from module_pptx.pptx_table.PptxTableCellBase import PptxTableCellBase


class PptxTableValueCell(PptxTableCellBase):
    def __init__(self, parameters, default_cell_style=None):
        super().__init__(parameters, default_cell_style)
        self._cell_style_input = None
        self._value_content = None
        self._value_format = None
        self._extractor.add_object("style", PptxCellStyle, description="")
        self._extractor.add_list("content", entry_type=dict, entry_object_type=PptxTextContent, description="")
        # Todo: Create a value format class with user friendly instructions
        self._extractor.add_str("value_format", description="This format is applied to the value before printing it to "
                                                            "the cell. For example '{:.2f}' rounds the value to 2 "
                                                            "decimals.")
        self._extractor.set_group_name("Presentation")

    def set_cell_value(self, value):
        self._value_content = [{
            "text": self.apply_format(value)
        }]

    def apply_format(self, value):
        if self._value_format is not None:
            return self._value_format.format(float(value))
        else:
            return str(value)

    def apply_styles(self, cell: _Cell):
        cell_style = PptxCellStyle(self._default_cell_style)
        cell_style.update_styles_by_input(self._cell_style_input)
        cell_style.generate()
        cell_style.apply_styles(cell)

        text_content = PptxTextContent(self._value_content, self._default_cell_style, cell.text_frame)
        text_content.update_styles_input(self._cell_style_input)
        text_content.apply_styles()

    def get_arguments(self):
        self._value_format = self._extractor.get_value("value_format")
        self._value_content = self._extractor.get_value("content")
        self._cell_style_input = self._extractor.get_value("style")

    def generate(self):
        self.extract()
        self.get_arguments()

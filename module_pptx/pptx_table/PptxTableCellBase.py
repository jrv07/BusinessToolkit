from pptx.table import _Cell
from module_misc.BasicTask import BasicTask


class PptxTableCellBase(BasicTask):
    def __init__(self, parameters, default_cell_style):
        super().__init__(parameters)
        self._default_cell_style = default_cell_style

    def set_cell_value(self, value):
        raise NotImplementedError

    def apply_styles(self, cell: _Cell):
        raise NotImplementedError

    def get_arguments(self):
        super().get_arguments()

    def generate(self):
        super().generate()


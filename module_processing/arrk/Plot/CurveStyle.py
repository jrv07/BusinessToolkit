from module_misc.BasicTask import BasicTask
from matplotlib.colors import ColorConverter


class CurveStyle(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._label = None
        self._color = None
        self._marker = None
        self._marker_size = None
        self._line_style = None
        self._line_width = None
        color_converter = ColorConverter()
        self._extractor.add_str("label", description="")
        self._extractor.add_str("color", valid_values=list(color_converter.colors.keys()), description="")
        self._extractor.add_str("marker", valid_values=['+', 'x', '|', ',', '.', 'o', 's'], description="")
        self._extractor.add_float("markersize", description="")
        self._extractor.add_str("linestyle", valid_values=['-', '--', '-.', ':'], description="")
        self._extractor.add_float("linewidth", description="")
        self._extractor.set_group_name("Processing.Arrk")

    @property
    def label(self):
        return self._label

    @property
    def color(self):
        return self._color

    @property
    def marker(self):
        return self._marker

    @property
    def marker_size(self):
        return self._marker_size

    @property
    def line_style(self):
        return self._line_style

    @property
    def line_width(self):
        return self._line_width

    def get_arguments(self):
        super().get_arguments()
        self._label = self._extractor.get_value("label")
        self._color = self._extractor.get_value("color")
        self._marker = self._extractor.get_value("marker")
        self._marker_size = self._extractor.get_value("markersize")
        self._line_style = self._extractor.get_value("linestyle")
        self._line_width = self._extractor.get_value("linewidth")

    def generate(self):
        self.extract()
        self.get_arguments()

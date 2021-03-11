from module_misc.BasicTask import BasicTask
from module_processing.arrk.CurveSelection import CurveSelection
from module_processing.arrk.Plot.CurveStyle import CurveStyle
from module_misc.Curve import Curve


class CurveDataBase(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._curve_style_input = None
        self._extractor.add_object("style", object_type=CurveStyle, optional=False, description="")
        self._extractor.set_group_name("Processing.Arrk")
        self._curve_style = None
        self._curve: Curve = None

    @property
    def curve_style(self) -> CurveStyle:
        return self._curve_style

    @property
    def curve(self) -> Curve:
        return self._curve

    def generate_curve_style(self):
        self._curve_style = CurveStyle(self._curve_style_input)
        self._curve_style.generate()

    def get_arguments(self):
        super().get_arguments()
        self._curve_style_input = self._extractor.get_value("style")

    def generate(self):
        super().generate()
        self.generate_curve_style()


class CurveData(CurveDataBase):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._selection_input = None
        self._extractor.add_object("selection", object_type=CurveSelection, optional=False, description="")
        self._selection = None

    def generate_curve_selection(self):
        self._selection = CurveSelection(self._selection_input)
        self._selection.generate()
        self._curve = self._selection.curve

    def get_arguments(self):
        super().get_arguments()
        self._selection_input = self._extractor.get_value("selection")

    def generate(self):
        self.extract()
        self.get_arguments()
        super().generate()
        self.generate_curve_selection()

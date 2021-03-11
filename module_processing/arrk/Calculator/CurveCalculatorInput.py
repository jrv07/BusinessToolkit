from module_misc.BasicTask import BasicTask
from module_processing.arrk.CurveSelection import CurveSelection


class CurveCalculatorInput(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._selection_input = None
        self._as = None
        self._extractor.add_object("selection", CurveSelection, optional=False, description="")
        self._extractor.add_str("as", optional=False, description="")
        self._extractor.set_group_name("Processing.Arrk")
        self._selection: CurveSelection = None

    @property
    def name(self):
        return self._as

    @property
    def curve(self):
        return self._selection.curve

    def generate_curve_selection(self):
        self._selection = CurveSelection(self._selection_input)
        self._selection.generate()

    def get_arguments(self):
        super().get_arguments()
        self._selection_input = self._extractor.get_value("selection")
        self._as = self._extractor.get_value("as")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_curve_selection()

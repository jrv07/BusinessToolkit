from module_processing.arrk.Plot.CurveData import CurveDataBase
from module_misc.Curve import Curve


class CurveDataTable(CurveDataBase):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._data_table = None
        self._line_number_x_values = None
        self._line_number_y_values = None
        self._x_label = None
        self._y_label = None
        self._extractor.add_source("variable", source_type=list, optional=False, description="")
        self._extractor.add_int("line_number_x_values", optional=False, description="")
        self._extractor.add_int("line_number_y_values", optional=False, description="")

    @property
    def x_label(self):
        return self._x_label

    @property
    def y_label(self):
        return self._y_label

    def generate_curve(self):
        print(self._data_table)
        count_lines = len(self._data_table[0])
        if self._line_number_x_values >= count_lines or self._line_number_y_values >= count_lines:
            print("data table doesn't contain enough lines")
            raise ValueError
        x_line = []
        y_line = []
        for col in self._data_table:
            x_line.append(col[self._line_number_x_values])
            y_line.append(col[self._line_number_y_values])
        self._x_label = x_line[0]
        x_values = x_line[1:]
        self._y_label = y_line[0]
        y_values = y_line[1:]
        self._curve = Curve("curve", x_values, y_values)

    def get_arguments(self):
        super().get_arguments()
        self._data_table = self._extractor.get_value("variable")
        print(self._parameters)
        self._line_number_x_values = self._extractor.get_value("line_number_x_values")
        self._line_number_y_values = self._extractor.get_value("line_number_y_values")

    def generate(self):
        self.extract()
        self.get_arguments()
        super().generate()
        self.generate_curve()

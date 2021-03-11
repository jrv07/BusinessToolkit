from module_misc.Curve import Curve
from typing import List
from module_input.Curve.CurveLoader import CurveLoader
from module_input.Curve.Csv.LoadCurvesSelectionCsv import LoadCurvesSelectionCsv
from module_input.Curve.Csv.LoadOptionsCsv import LoadOptionsCsv
from pandas import read_csv, isnull, DataFrame
import os


class CurveLoaderCsv(CurveLoader):
    def __init__(self, file_path, curve_selections: List[LoadCurvesSelectionCsv],
                 options: LoadOptionsCsv, log_curve_tags=False):
        super().__init__(file_path, log_curve_tags)
        self._csv_content: DataFrame = None
        self._curve_extractions = curve_selections
        self._curve_titles = None
        self._options = options

    def read_file(self):
        separator = self._options.separator
        header = self._options.header
        nrows = self._options.number_rows
        decimal = self._options.decimal_specifier
        comment = self._options.comment_specifier
        error_bad_lines = self._options.error_bad_lines
        skip_rows = self._options.skip_rows
        csv_content = read_csv(self._file_path, sep=separator, header=header, nrows=nrows, skip_blank_lines=True, decimal=decimal, comment=comment, error_bad_lines=error_bad_lines, skiprows=skip_rows)
        number_columns = csv_content.shape[1]
        if isnull(csv_content.iloc[:, number_columns - 1]).all():
            csv_content = csv_content.drop(csv_content.columns[[number_columns - 1]], axis=1)
        self._csv_content = csv_content

    def read_all_curve_titles(self, content: list):
        columns = list(self._csv_content.columns)
        self._curve_titles = columns[1:]
        for curve_title in self._curve_titles:
            curve_description = "  - curve_title: \"{}\"".format(curve_title)
            content.append(curve_description)

    def log_curve_tags(self):
        if self._log_curve_tags:
            from extra_functions import write_file
            from share_objects import curvesDir
            content = ["curve_extractions:"]
            self.read_all_curve_titles(content)
            file_name = "{}.log".format(os.path.basename(self._file_path))
            write_file(os.path.join(curvesDir, file_name), "\n".join(content))

    def is_curve_requested(self, curve_title: str):
        for ct in self._curve_titles:
            if ct == curve_title:
                return True
        return False

    def generate_curves(self):
        columns = list(self._csv_content.columns)
        number_columns = self._csv_content.shape[1]
        for column_id in range(1, number_columns):
            curve_title = columns[column_id]
            if self.is_curve_requested(curve_title):
                x_values = self._csv_content.iloc[:, 0]
                y_values = self._csv_content.iloc[:, column_id]
                curve = Curve(curve_title, x_values, y_values)
                self._curves.add_curve(curve, curve_title)

    def generate(self):
        self.read_file()
        self.log_curve_tags()
        self.generate_curves()

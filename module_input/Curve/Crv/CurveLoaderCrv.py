import logging
from module_misc.Curve import Curve
from typing import List
from module_input.Curve.CurveLoader import CurveLoader
from module_input.Curve.Crv.LoadCurvesSelectionCrv import LoadCurvesSelectionCrv
import re
import os


class CurveLoaderCrv(CurveLoader):
    def __init__(self, file_path, curve_selections: List[LoadCurvesSelectionCrv], log_curve_tags=False):
        super().__init__(file_path, log_curve_tags)
        self._crv_content: list = None
        self._curve_extractions = curve_selections
        self._curve_titles = None

    def read_file(self):
        with open(self._file_path) as f:
            self._crv_content = f.readlines()

    def read_all_curve_titles(self, content: list):
        index = 0
        while index < len(self._crv_content):
            count_header_lines, count_data_lines = self.get_curve_data_line_counts(index)
            curve_title = self.get_curve_title(index + 1, count_header_lines)
            curve_description = "  - curve_title: \"{}\"".format(curve_title)
            content.append(curve_description)
            index += 1 + count_header_lines + count_data_lines

    def log_curve_tags(self):
        if self._log_curve_tags:
            from extra_functions import write_file
            from share_objects import curvesDir
            content = ["curve_extractions:"]
            self.read_all_curve_titles(content)
            file_name = "{}.log".format(os.path.basename(self._file_path))
            write_file(os.path.join(curvesDir, file_name), "\n".join(content))

    def generate_curve_titles_list(self):
        curve_titles = []
        for curve_extraction in self._curve_extractions:
            curve_titles.append(curve_extraction.curve_title)
        self._curve_titles = curve_titles

    def get_curve_data_line_counts(self, index):
        match_curve_definition_line = re.match(r'^(.+)CurveFileDat(.+)$', self._crv_content[index], re.I)
        if not match_curve_definition_line:
            raise Exception("unable to find CurveFileDat in line {}".format(index))
        count_header_lines = int(match_curve_definition_line.group(2))
        count_data_lines = int(match_curve_definition_line.group(1))
        return count_header_lines, count_data_lines

    def get_curve_title(self, index_header_start: int, count_header_lines: int):
        index_header_end = index_header_start + count_header_lines
        for line in self._crv_content[index_header_start:index_header_end]:
            match_title_line = re.match(r'^Title\s*(.+)\s*$', line, re.I)
            if match_title_line:
                return match_title_line.group(1)
        logging.error("No curve title found in lines [{}:{}]".format(index_header_start, index_header_end))
        raise ValueError

    def is_curve_requested(self, curve_title: str):
        for ct in self._curve_titles:
            if ct == curve_title:
                return True
        return False

    def generate_curve_data(self, index_data_start: int, count_data_lines: int, curve_title: str) -> Curve:
        index_data_end = index_data_start + count_data_lines
        x_values = []
        y_values = []
        for line in self._crv_content[index_data_start:index_data_end]:
            match_data_line = re.match(r'^\s*([^\s]+)\s+([^\s]+)\s*$', line)
            x_values.append(float(match_data_line.group(1)))
            y_values.append(float(match_data_line.group(2)))
        return Curve(curve_title, x_values, y_values)

    def generate_curves(self):
        self.generate_curve_titles_list()
        index = 0
        while index < len(self._crv_content):
            count_header_lines, count_data_lines = self.get_curve_data_line_counts(index)
            index_header_start = index + 1
            index_data_start = index_header_start + count_header_lines
            curve_title = self.get_curve_title(index_header_start, count_header_lines)
            if self.is_curve_requested(curve_title):
                curve = self.generate_curve_data(index_data_start, count_data_lines, curve_title)
                self._curves.add_curve(curve, curve_title)
            index += 1 + count_header_lines + count_data_lines

    def generate(self):
        self.read_file()
        self.log_curve_tags()
        self.generate_curves()

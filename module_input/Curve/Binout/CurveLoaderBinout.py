import logging
import os
from lasso.dyna.Binout import Binout
from textwrap import wrap
import numpy
from module_misc.Curve import Curve
from typing import List
from module_input.Curve.CurveLoader import CurveLoader
from module_input.Curve.Binout.LoadCurvesSelectionBinout import LoadCurvesSelectionBinout


class CurveLoaderBinout(CurveLoader):
    def __init__(self, file_path, curve_selections: List[LoadCurvesSelectionBinout], log_curve_tags=False):
        super().__init__(file_path, log_curve_tags)
        self._binout_content: Binout = None
        self._curve_extractions = curve_selections

    def get_binout_prefix(self, basename):
        try:
            binout_name = basename.split("binout")[0] + "binout*"
            print("reading binout : {}".format(binout_name))
        except Exception as exception:
            logging.error("'{}' doesn't exist".format(str(basename)))
            raise ValueError
        return binout_name

    def read_file(self):
        binout_path = os.path.dirname(self._file_path)
        binout_base_name = os.path.basename(self._file_path)
        prefix = self.get_binout_prefix(binout_base_name)
        binout_files = os.path.join(binout_path, prefix)
        self._binout_content = Binout(binout_files)

    @staticmethod
    def get_curve_path_representation(curve_path_list: List[str]) -> str:
        curve_path_list_quoted_entries = list(map(lambda cp: "\"{}\"".format(cp), curve_path_list))
        return "[{}]".format(", ".join(curve_path_list_quoted_entries))

    def get_curve_description(self, path: List[str]):
        last_path_index = len(path) - 1
        curve_path = self.get_curve_path_representation(path[:last_path_index])
        function_name = path[last_path_index]
        tag = self.create_tag(path[:last_path_index], function_name)
        return "curve_path: {}, function_name: \"{}\" -> tag: {}".format(curve_path, function_name, tag)

    def read_curve_paths_recursive(self, content: list, data=None, path: list = None):
        if data is None:
            self.read_curve_paths_recursive(content, self._binout_content.read(), [])
        else:
            if isinstance(data, numpy.ndarray):
                content.append(self.get_curve_description(path))
            elif isinstance(data, list):
                for entry in data:
                    if entry not in ["legend", "legend_ids", "ids"]:
                        next_path = [*path, entry]
                        try:
                            self.read_curve_paths_recursive(content, self._binout_content.read(*path, entry), next_path)
                        except:
                            content.append("Error in data {}".format(".".join(next_path)))

    def log_curve_tags(self):
        # Todo: store possible ids in this file too if existing
        if self._log_curve_tags:
            from extra_functions import write_file
            from share_objects import curvesDir
            content = []
            self.read_curve_paths_recursive(content)
            file_name = "{}.log".format(os.path.basename(self._file_path))
            write_file(os.path.join(curvesDir, file_name), "\n".join(content))

    def get_legends_array(self, path) -> list:
        legend_string = self._binout_content.read(*path, "legend")
        if legend_string is None:
            return []
        legends = wrap(legend_string, 80)
        return list(map(lambda legend: legend.strip(), legends))

    def read_numpy_ndarray_values_from_path(self, expected_dimensions: list, *path):
        print("reading {}".format(path))
        try:
            values = self._binout_content.read(*path)
        except Exception as exception:
            logging.error("'{}' doesn't exist".format(str(*path)))
            raise ValueError
        if not isinstance(values, numpy.ndarray):
            logging.error("result is of type {} instead of numpy.ndarray".format(type(values)))
            raise ValueError
        if values.ndim not in expected_dimensions:
            logging.error("dimension not as expected. Expected dimension: {}, current dimension: {}"
                          .format(expected_dimensions, values.ndim))
            raise ValueError
        return values

    def get_indices_to_ids(self, content: list, path: list, requested_ids: list = None):
        if "ids" not in content:
            print("ids doesn't exist under this path")
            raise ValueError
        all_ids = list(self._binout_content.read(*path, "ids"))
        if requested_ids is not None:
            indices = []
            for id_value in requested_ids:
                indices.append(all_ids.index(id_value))
        else:
            indices = range(0, len(all_ids)-1)
        return all_ids, indices

    def get_curve_name(self, path: list, function_name, requested_id=None, requested_index=None):
        content = self._binout_content.read(*path)
        # print(content)
        curve_name_parts = []
        if "title" in content:
            curve_name_parts.append(self._binout_content.read(*path, "title").strip())
        category_name = self.get_category_name(path[0])
        curve_name_parts.append(category_name)
        if requested_id is not None and requested_index is not None:
            if "legend_ids" in content and "legend" in content:
                legend = self.get_legends_array(path)
                legend_ids = self._binout_content.read(*path, "legend_ids")
                if requested_index >= len(legend_ids):
                    curve_name_parts.append(str(requested_id))
                else:
                    curve_name_parts.append(legend[requested_index])
            else:
                curve_name_parts.append(str(requested_id))
        curve_name_parts.append(function_name)
        return "_".join(curve_name_parts)

    @staticmethod
    def create_tag(path, function, requested_id=None):
        if requested_id is None:
            return "{}.{}".format(".".join(path), function)
        else:
            return "{}.{}.{}".format(".".join(path), function, requested_id)

    def generate_curves_specific_function(self, function, path: list, curve_content, x_values, all_ids, requested_indices):
        if function not in curve_content:
            print("no '{}' available under this path. Current content: {}".format(function, curve_content))
            return None

        y_values = self.read_numpy_ndarray_values_from_path([1, 2], *path, function)

        if y_values.ndim == 1:
            curve_name = self.get_curve_name(path, function)
            curve = Curve(curve_name, x_values, y_values)
            tag = self.create_tag(path, function)
            self._curves.add_curve(curve, tag)
        elif y_values.ndim == 2:
            if all_ids is None:
                print("no 'ids' available under this path. Current content: {}".format(curve_content))
                return None
            for ind in requested_indices:
                curve_name = self.get_curve_name(path, function, all_ids[ind], ind)
                curve = Curve(curve_name, x_values, y_values[..., ind])
                tag = self.create_tag(path, function, all_ids[ind])
                self._curves.add_curve(curve, tag)

    def generate_curves_from_extraction_data(self, curve_extraction: LoadCurvesSelectionBinout):
        path = curve_extraction.curve_path
        function_names = curve_extraction.function_names
        curve_content = self._binout_content.read(*path)
        if "time" not in curve_content:
            print("no time values available under this path. Current content: {}".format(curve_content))
            raise ValueError
        time_values = self.read_numpy_ndarray_values_from_path([1], *path, "time")

        all_ids = None
        requested_indices = None
        if "ids" in curve_content:
            all_ids, requested_indices = self.get_indices_to_ids(curve_content, path, curve_extraction.requested_ids)

        for function_name in function_names:
            self.generate_curves_specific_function(function_name, path, curve_content,
                                                   time_values, all_ids, requested_indices)

    @staticmethod
    def get_category_name(category):
        # Todo: find out all corresponding names
        if category == "nodout":
            return "Node"
        elif category == "jntforc":
            return "Joint"
        elif category == "deforc":
            return "Spring / Damper"
        elif category == "elout":
            return "Elements"
        elif category == "abstat":
            return "Airbag"
        elif category == "swforc":
            return ""
        elif category == "sleout":
            return ""
        elif category == "secforc":
            return "Section"
        elif category == "rcforc":
            return "Contact Forces"
        elif category == "matsum":
            return ""
        elif category == "glstat":
            return "Global"

    def generate_curves(self):
        for curve_extraction in self._curve_extractions:
            self.generate_curves_from_extraction_data(curve_extraction)

    def generate(self):
        self.read_file()
        self.log_curve_tags()
        self.generate_curves()

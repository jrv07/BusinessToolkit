from module_misc.RegisterData import RegisterFile
from module_misc.WithStoreData import WithStoreData
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from module_processing.arrk.Plot.CurveData import CurveData, CurveDataBase
from module_processing.arrk.Plot.CurveDataTable import CurveDataTable
from typing import List
import os


class CurvePlot(WithStoreData):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._title = None
        self._file_name = None
        self._x_label = None
        self._y_label = None
        self._x_units = None
        self._y_units = None
        self._legend = None
        self._grid = None
        self._font_size = None
        self._title_font_size = None
        self._legend_font_size = None
        self._fig_size = None
        self._transparent = None
        self._curves_input = None
        self._data_table_input = None
        self._data_table = None
        self._extractor.add_str("filename", optional=False, description="")
        self._extractor.add_list("curves", entry_type=dict, entry_object_type=CurveData, optional=False,
                                 alternative="table_data", description="")
        self._extractor.add_object("table_data", object_type=CurveDataTable, optional=False, description="")
        self._extractor.add_str("title", optional=False, default="", description="")
        self._extractor.add_str("xlabel", optional=False, default="", description="")
        self._extractor.add_str("ylabel", optional=False, default="", description="")
        self._extractor.add_str("xunits", description="")
        self._extractor.add_str("yunits", description="")
        self._extractor.add_bool("legend", description="")
        self._extractor.add_bool("grid", optional=False, default=True, description="")
        self._extractor.add_float("fontsize", optional=False, default="None", description="")
        self._extractor.add_float("titlefontsize", description="")
        self._extractor.add_float("legendfontsize", description="")
        self._extractor.add_list("figsize", entry_type=float, length=2, description="")
        self._extractor.add_bool("transparent", optional=False, default=False, description="")
        self._extractor.set_group_name("Processing.Arrk")

        self._curves: List[CurveData] = []
        self._curve_data_table: CurveDataTable = None
        self._figure: Figure = None
        self._axes: Axes = None
        self._file_path = None

    def generate_file_path(self):
        from share_objects import plotsDir
        self._file_path = os.path.join(plotsDir, self._file_name)

    def generate_all_font_sizes(self):
        if self._title_font_size is None:
            self._title_font_size = self._font_size
        if self._legend_font_size is None:
            self._legend_font_size = self._font_size

    @staticmethod
    def get_ax_description(label, units):
        if label is not None:
            if units is not None:
                return "{} [{}]".format(label, units)
            else:
                return label
        else:
            if units is not None:
                return "[{}]".format(units)
            else:
                return ""

    def initialize_plot(self):
        self._figure = Figure(figsize=self._fig_size)
        self._axes = self._figure.add_subplot()

    def add_curves_to_plot(self):
        if len(self._curves) > 0:
            for curve_data in self._curves:
                self.add_curve_to_plot(curve_data)
        else:
            self.add_curve_to_plot(self._curve_data_table)

    def add_curve_to_plot(self, curve_data_base: CurveDataBase):
        curve = curve_data_base.curve
        data_frame = curve.df
        color = curve_data_base.curve_style.color
        label = curve_data_base.curve_style.label
        marker = curve_data_base.curve_style.marker
        marker_size = curve_data_base.curve_style.marker_size
        line_width = curve_data_base.curve_style.line_width
        line_style = curve_data_base.curve_style.line_style
        self._axes = data_frame.plot(ax=self._axes, x=0, y=1, color=color, legend=self._legend, label=label,
                                     marker=marker, fontsize=self._font_size, linewidth=line_width,
                                     linestyle=line_style, markersize=marker_size, grid=self._grid)

    def finalize_plot(self):
        if self._title is not None:
            self._axes.set_title(self._title, fontsize=self._title_font_size)
        x_label = self.get_ax_description(self._x_label, self._x_units)
        y_label = self.get_ax_description(self._y_label, self._y_units)
        self._axes.set_xlabel(x_label, fontsize=self._font_size)
        self._axes.set_ylabel(y_label, fontsize=self._font_size)
        if self._legend is not None:
            if self._legend:
                self._axes.legend(fontsize=self._legend_font_size)

        self._figure.savefig(self._file_path, transparent=self._transparent)

    def generate_figure(self):
        self.initialize_plot()
        self.add_curves_to_plot()
        self.finalize_plot()

    def generate_store_data(self):
        self._store_data = RegisterFile(self._file_path)

    def generate_curves(self):
        if self._curves_input is not None:
            for curve_input in self._curves_input:
                curve_data = CurveData(curve_input)
                curve_data.generate()
                self._curves.append(curve_data)
        else:
            curve_data_table = CurveDataTable(self._data_table_input)
            curve_data_table.generate()
            self._curve_data_table = curve_data_table
            self._x_label = self._curve_data_table.x_label
            self._y_label = self._curve_data_table.y_label

    def get_arguments(self):
        super().get_arguments()
        self._title = self._extractor.get_value("title")
        self._file_name = self._extractor.get_value("filename")
        self._x_label = self._extractor.get_value("xlabel")
        self._y_label = self._extractor.get_value("ylabel")
        self._x_units = self._extractor.get_value("xunits")
        self._y_units = self._extractor.get_value("yunits")
        self._legend = self._extractor.get_value("legend")
        self._grid = self._extractor.get_value("grid")
        self._font_size = self._extractor.get_value("fontsize")
        self._title_font_size = self._extractor.get_value("titlefontsize")
        self._legend_font_size = self._extractor.get_value("legendfontsize")
        self._fig_size = self._extractor.get_value("figsize")
        self._transparent = self._extractor.get_value("transparent")
        self._curves_input = self._extractor.get_value("curves")
        if self._curves_input is None:
            self._data_table_input = self._extractor.get_value("table_data")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_file_path()
        self.generate_all_font_sizes()
        self.generate_curves()
        self.generate_figure()
        self.generate_store_data()
        self.store_in_register()

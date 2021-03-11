import logging
import scipy.signal as signal
from scipy.signal import butter
from module_misc.Curve import Curve
from module_misc.Curves import Curves
from pandas import DataFrame
from numpy import array as np_array
from module_processing.arrk.Calculator.Calculation.Instructions.CurveCalculationInstruction import \
    CurveCalculationInstruction


class CurveCalculationInstructionFilter(CurveCalculationInstruction):
    def __init__(self, parameters):
        super().__init__(parameters, "filter", in_min_length_required=1, out_equals_in_length=True)
        self._type = None
        valid_types = ["cfc60", "cfc180", "cfc600", "cfc1000"]
        self._extractor.add_str("type", valid_values=valid_types, optional=False, description="")

    # def extract_type(self):
    #     valid_types = ["cfc60", "cfc180", "cfc600", "cfc1000"]
    #     self._type = extract_value_str("type", self._parameters, valid_values=valid_types, optional=False)

    @staticmethod
    def apply_butterworth_filter(data, sampling_freq, limit_freq):
        nyq = 0.5 * sampling_freq
        low = limit_freq / nyq
        b, a = butter(2, low, "lowpass", analog=False)
        return signal.filtfilt(b, a, data)

    def apply_filter(self, data_frame):
        curve_filter = self._type
        if curve_filter is None:
            return data_frame.copy()
        if curve_filter == "cfc600":
            sampling_freq = 6000
            limit_freq = 1000
        elif curve_filter == "cfc180":
            sampling_freq = 1800
            limit_freq = 300
        elif curve_filter == "cfc60":
            sampling_freq = 600
            limit_freq = 100
        elif curve_filter == "cfc1000":
            sampling_freq = 10000
            limit_freq = 1650
        else:
            logging.error("unknown filter")
            raise ValueError
        y_values = self.apply_butterworth_filter(data_frame.Y, sampling_freq, limit_freq)
        result_df = DataFrame({"X": np_array(data_frame.X, dtype=float),
                              "Y": np_array(y_values, dtype=float)})
        return result_df

    def apply_modification(self, curve: Curve) -> Curve:
        data_frame = curve.df
        result_df = self.apply_filter(data_frame)
        result_curve = Curve(curve.name, result_df.X, result_df.Y)
        return result_curve

    def calculate(self, curves: Curves, values: dict):
        for curve_index, curve_name in enumerate(self._curve_names):
            curve_filter = curves.get_curve(curve_name)
            curve_filter = self.apply_modification(curve_filter)
            curves.add_curve(curve_filter, self._result_curves[curve_index])

    def get_arguments(self):
        super().get_arguments()
        self._type = self._extractor.get_value("type")

    def generate(self):
        # self.extract_type()
        self.extract()
        self.get_arguments()


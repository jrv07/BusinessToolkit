from numpy import array as np_array, log as np_log, exp as np_exp
from pandas import DataFrame


class Curve:
    def __init__(self, name, x_values, y_values, x_units='', y_units='', iso_name='', element_id=0):
        self._name = name
        if any(type(x) == str for x in x_values):
            x_type = str
        else:
            x_type = float
        if any(type(y) == str for y in y_values):
            y_type = str
        else:
            y_type = float
        self._df = DataFrame({"X": np_array(x_values, dtype=x_type),
                             "Y": np_array(y_values, dtype=y_type)})
        self._x_units = x_units
        self._y_units = y_units
        self._iso_name = iso_name
        self._element_id = element_id

    @property
    def name(self):
        return self._name

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, new_df):
        self._df = new_df

    @property
    def x_units(self):
        return self._x_units

    @property
    def y_units(self):
        return self._y_units

    @property
    def iso_name(self):
        return self._iso_name

    @property
    def element_id(self):
        return self._element_id

    def __add__(self, other: "Curve"):
        result_df = self._df + other.df
        return Curve("", self._df.X, result_df.Y)

    def __sub__(self, other: "Curve"):
        result_df = self._df - other.df
        return Curve("", self._df.X, result_df.Y)

    def __mul__(self, other: "Curve"):
        result_df = self._df * other.df
        return Curve("", self._df.X, result_df.Y)

    def __truediv__(self, other: "Curve"):
        result_df = self._df.truediv(other.df)
        return Curve("", self._df.X, result_df.Y)

    def __pow__(self, power: float):
        result_df = self._df.pow(power)
        return Curve("", self._df.X, result_df.Y)

    def logarithmize(self):
        result_df = np_log(self._df)
        return Curve("", self._df.X, result_df.Y)

    def exponentiate(self):
        result_df = np_exp(self._df)
        return Curve("", self._df.X, result_df.Y)

    def min(self):
        return self._df.Y.values.min()

    def max(self):
        return self._df.Y.values.max()

    def __str__(self):
        header_data = [
            "Name: {}".format(self.name),
            "x units: {}".format(self.x_units),
            "y units: {}".format(self.y_units),
            "iso name: {}".format(self.iso_name),
            "element id: {}".format(self.element_id)
        ]
        header = "\n".join(header_data)
        data = self.df.to_string
        return "\n\n".join([header, data])


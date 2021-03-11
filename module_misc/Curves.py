import logging
from module_misc.Curve import Curve


class Curves:
    def __init__(self):
        self._curves_data = []

    @property
    def data(self):
        # print("reading {}".format(self._curves_data))
        return self._curves_data

    def get_curve(self, tag: str) -> Curve:
        # print(self._curves_data)
        for curve_entry in self._curves_data:
            if curve_entry["tag"] == tag:
                return curve_entry["curve"]
        logging.error("curve with tag {} does not exist.".format(tag))
        raise ValueError

    def add_curve(self, curve: Curve, tag: str):
        for curve_entry in self._curves_data:
            if curve_entry["tag"] == tag:
                logging.error("curve with this tag already exists")
                raise ValueError
        self._curves_data.append({
            "tag": tag,
            "curve": curve
        })

from module_misc.Curves import Curves


class CurveLoader:
    def __init__(self, file_path, log_curve_tags=False):
        self._file_path = file_path
        self._log_curve_tags = log_curve_tags
        self._curves = Curves()

    @property
    def curves(self):
        return self._curves

    def read_file(self):
        raise NotImplementedError

    def log_curve_tags(self):
        raise NotImplementedError

    def generate_curves(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError

from module_misc.BasicTask import BasicTask


class LoadOptionsCsv(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._header = None
        self._number_rows = None
        self._decimal_specifier = None
        self._comment_specifier = None
        self._error_bad_lines = None
        self._separator = None
        self._skip_rows = None
        self._extractor.add_str("header", optional=False, default="infer", description="")
        self._extractor.add_int("number_rows", description="")
        self._extractor.add_str("decimal_specifier", optional=False, default=".", description="")
        self._extractor.add_str("comment_specifier", description="")
        self._extractor.add_bool("error_bad_lines", optional=False, default=True, description="")
        self._extractor.add_str("separator", optional=False, default=",", description="")
        self._extractor.add_list("skip_rows", entry_type=int, description="")
        self._extractor.set_group_name("ReadData")

    @property
    def header(self):
        return self._header

    @property
    def number_rows(self):
        return self._number_rows

    @property
    def decimal_specifier(self):
        return self._decimal_specifier

    @property
    def comment_specifier(self):
        return self._comment_specifier

    @property
    def error_bad_lines(self):
        return self._error_bad_lines

    @property
    def separator(self):
        return self._separator

    @property
    def delimiter(self):
        return self._separator

    @property
    def skip_rows(self):
        return self._skip_rows

    def get_arguments(self):
        super().get_arguments()
        self._header = self._extractor.get_value("header")
        self._number_rows = self._extractor.get_value("number_rows")
        self._decimal_specifier = self._extractor.get_value("decimal_specifier")
        self._comment_specifier = self._extractor.get_value("comment_specifier")
        self._error_bad_lines = self._extractor.get_value("error_bad_lines")
        self._separator = self._extractor.get_value("separator")
        self._skip_rows = self._extractor.get_value("skip_rows")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()

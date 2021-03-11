from module_misc.BasicTask import BasicTask
from module_misc.RegisterData import RegisterCalculationData


class PptxFromVariable(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._data = None
        self._path = []
        self._value = None
        self._extractor.add_source("variable", source_type=RegisterCalculationData, optional=False, description="")
        self._extractor.add_list("path", entry_object_type=str, description="")
        self._extractor.set_group_name("Presentation")

    @property
    def value(self):
        return self._value

    def generate_value(self):
        value = self._data
        if self._path is not None:
            for path_entry in self._path:
                value = value[path_entry]
        self._value = str(value)

    def get_arguments(self):
        super().get_arguments()
        register_calculation_data: RegisterCalculationData = self._extractor.get_value("variable")
        self._data = register_calculation_data.values
        print(self._data)
        self._path = self._extractor.get_value("path")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_value()

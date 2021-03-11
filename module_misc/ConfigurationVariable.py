from module_misc.BasicTask import BasicTask


class ConfigurationVariableData:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str({
            self._name: self._value
        })

    def __copy__(self):
        return ConfigurationVariableData(self.name, self.value)


class ConfigurationVariable(BasicTask):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._name = None
        self._value = None
        self._extractor.add_str("name", optional=False, description="")
        self._extractor.add_float("value_float", specifier="value", optional=False, alternative="value_str", description="")
        self._extractor.add_str("value_str", specifier="value", optional=False, description="")
        self._extractor.set_group_name("Misc")
        self._data: ConfigurationVariableData = None

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._data.name

    @property
    def value(self):
        return self._data.value

    def __str__(self):
        return str(self.data)

    def get_arguments(self):
        super().get_arguments()
        self._name = self._extractor.get_value("name")
        self._value = self._extractor.get_value("value_float")
        if self._value is None:
            self._value = self._extractor.get_value("value_str")

    def generate_variable_data(self):
        self._data = ConfigurationVariableData(self._name, self._value)

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_variable_data()

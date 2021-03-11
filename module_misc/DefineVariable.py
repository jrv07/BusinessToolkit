from module_misc.WithStoreData import WithStoreData
from module_misc.DefinableObjectsFactory import DefinableObjectsFactory


class DefineVariable(WithStoreData):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._definition_input = None
        self._extractor.add_object("definition", DefinableObjectsFactory, optional=False, description="")
        self._extractor.set_group_name("Misc")
        self._definition: DefinableObjectsFactory = None

    def generate_store_data(self):
        self._store_data = self._definition.instruction

    def generate_definition(self):
        self._definition = DefinableObjectsFactory(self._definition_input)
        self._definition.generate()

    def get_arguments(self):
        super().get_arguments()
        self._definition_input = self._extractor.get_value("definition")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_definition()
        self.generate_store_data()
        self.store_in_register()

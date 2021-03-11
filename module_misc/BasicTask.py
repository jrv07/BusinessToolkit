from module_misc.Extractor import Extractor


class BasicTask:
    def __init__(self, parameters, settings=None):
        self._extractor: Extractor = Extractor(self.__class__.__name__)
        self._parameters = parameters
        self._settings = settings

    @property
    def store_data(self):
        return None

    @property
    def class_name(self):
        return self._extractor.class_name

    def get_arguments(self):
        pass

    def extract(self):
        self._extractor.extract(self._parameters)

    def get_structure(self):
        return self._extractor.get_structure()

    def generate(self):
        pass

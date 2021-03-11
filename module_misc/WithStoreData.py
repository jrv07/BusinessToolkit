import logging
from module_misc.BasicTask import BasicTask


class WithStoreData(BasicTask):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._register_name_from_parameters = None
        self._extractor.add_str("register", description="")
        self._register_name = None
        self._store_data = None

    @property
    def store_data(self):
        return self._store_data

    def store_in_register(self):
        if self._register_name is not None:
            from share_objects import register
            if register.get(self._register_name, None) is not None:
                logging.error("register name already set! Choose a unique name. Current name: {}"
                              .format(self._register_name))
                raise ValueError
            register[self._register_name] = self._store_data

    def generate_register_name(self):
        if self._settings is not None:
            if "register" in self._settings:
                self._register_name = self._settings["register"]
        if self._register_name is None:
            self._register_name = self._register_name_from_parameters

    def get_arguments(self):
        super().get_arguments()
        self._register_name_from_parameters = self._extractor.get_value("register")
        self.generate_register_name()

    def generate_store_data(self):
        raise NotImplementedError

    def generate(self):
        super().generate()

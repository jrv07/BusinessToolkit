from module_misc.BasicTask import BasicTask


class PptxStyle(BasicTask):
    def __init__(self, parameters=None):
        super().__init__(parameters)
        self._parameters = None
        if parameters is not None:
            self._parameters = dict(parameters)

    def update_styles_by_input(self, styles_input):
        if styles_input is not None:
            if self._parameters is not None:
                self._parameters.update(styles_input)
            else:
                self._parameters = styles_input

    def update_styles_by_object(self, styles_object):
        raise NotImplementedError

    def set_parameters(self, parameters):
        self._parameters = parameters

    def get_arguments(self):
        super().get_arguments()

    def generate(self):
        super().generate()

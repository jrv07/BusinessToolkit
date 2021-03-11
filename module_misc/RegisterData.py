class RegisterData:
    def __init__(self):
        pass


class RegisterPostProcessorInstructionData(RegisterData):
    def __init__(self, commands):
        super().__init__()
        self._commands = commands

    @property
    def commands(self):
        return self._commands


class RegisterPostProcessorWriteInstructionData(RegisterPostProcessorInstructionData):
    def __init__(self, commands, file_path):
        super().__init__(commands)
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path


class RegisterFile(RegisterData):
    def __init__(self, file_path):
        super().__init__()
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path


class RegisterCalculationData:
    def __init__(self, curves: "Curves" = None, values: dict = None):
        self._curves: "Curves" = curves
        self._values: dict = values

    @property
    def curves(self):
        return self._curves

    @property
    def values(self):
        return self._values

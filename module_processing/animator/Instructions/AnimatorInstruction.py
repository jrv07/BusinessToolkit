from module_misc.WithStoreData import WithStoreData
from module_misc.RegisterData import RegisterPostProcessorInstructionData


class AnimatorInstruction(WithStoreData):
    def __init__(self, parameters):
        super().__init__(parameters)
        self._commands = []
        self._source: RegisterPostProcessorInstructionData = None
        self._extractor.add_source("source", source_type=RegisterPostProcessorInstructionData, is_dominant=True,
                                   description="source instruction_name")
        self._extractor.set_group_name("Processing.Animator")

    @staticmethod
    def prepare_path_for_animator_script(file_path):
        from share_objects import current_platform_system
        if current_platform_system == "Windows":
            return file_path.replace('\\', '\\\\\\\\')
        else:
            return file_path

    @property
    def commands(self):
        return self._commands

    def add_command(self, command):
        self._commands.append(command)

    def add_commands(self, commands):
        self._commands.extend(commands)

    def check_source(self):
        if self._source is not None:
            self._commands = self._source.commands
            return True
        return False

    @staticmethod
    def get_on_off(value: bool) -> str:
        if value:
            return "on"
        else:
            return "off"

    def get_arguments(self):
        super().get_arguments()
        self._source = self._extractor.get_value("source")

    def generate_store_data(self):
        self._store_data = RegisterPostProcessorInstructionData(self._commands)

    def generate(self):
        super().generate()

    def post_animator_run(self):
        pass

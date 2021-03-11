import subprocess
import logging
import os
from module_processing.metapost.MetapostInstructionFactory import MetapostInstructionFactory
from module_misc.WithStoreData import WithStoreData
from module_misc.BasicTask import BasicTask
from module_processing.metapost.MetapostSettings import MetapostSettings
from module_processing.PostProcessorScript import PostProcessorScript
from module_processing.metapost.MetapostScript import MetapostPythonScript, MetapostSessionFile


class MetapostTask(WithStoreData):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._session_name = None
        self._script = PostProcessorScript()
        self._script_flag = ""
        self._metapost_settings_input = None
        self._metapost_settings: MetapostSettings = None
        self._instructions_input = None
        self._extractor.add_str("session_name", optional=False, description="")
        self._extractor.add_object("settings", MetapostSettings, optional=False, description="")
        self._extractor.add_list("instructions", entry_type=dict, entry_object_type=MetapostInstructionFactory,
                                 optional=False, description="")
        self._extractor.set_group_name("Processing.Metapost")
        self._instructions = []

    def save_script(self):
        self._script.save()

    def start_metapost_with_script(self):
        start_command = ['"{}"'.format(self._metapost_settings.version), self._script_flag, self._script.file_name]
        if self._metapost_settings.options is not None:
            start_command.append(self._metapost_settings.options)
        self.start_subprocess(" ".join(start_command))

    @staticmethod
    def start_subprocess(start_command):
        logging.info('command: "{}"'.format(start_command))
        proc = subprocess.run(args=start_command, stdout=subprocess.PIPE, shell=True)  #, universal_newlines=True)#text=True,
        returncode = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
        proc.check_returncode()

    def add_command(self, command):
        self._script.add_command(command)

    def add_commands(self, command_list):
        self._script.add_commands(command_list)

    def generate_settings(self):
        self._metapost_settings = MetapostSettings(self._metapost_settings_input)
        self._metapost_settings.generate()
        from share_objects import metapostDir
        script_type = self._metapost_settings.script_type
        if script_type == "python":
            self._script = MetapostPythonScript(os.path.join(metapostDir, str(self._session_name) + '.py'))
            self._script_flag = "-exec"
        elif script_type == "session":
            self._script = MetapostSessionFile(os.path.join(metapostDir, str(self._session_name) + '.ses'))
            self._script_flag = "-s"

    def generate_instructions(self):
        for instruction_input in self._instructions_input:
            instruction = MetapostInstructionFactory(instruction_input)
            instruction.generate()
            self.add_commands(instruction.commands)
            self._instructions.append(instruction.instruction)

    def generate_store_data(self):
        self._store_data = self

    def get_arguments(self):
        super().get_arguments()
        self._metapost_settings_input = self._extractor.get_value("settings")
        self._instructions_input = self._extractor.get_value("instructions")
        self._session_name = self._extractor.get_value("session_name")

    def generate(self):
        self.extract()
        self.get_arguments()
        self.generate_settings()
        self.generate_instructions()
        self.generate_store_data()
        self.store_in_register()

    def post_run(self):
        for instruction in self._instructions:
            instruction.post_metapost_run()


class MetapostRun(BasicTask):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._task: MetapostTask = None
        self._dry = None
        self._extractor.add_source("task", source_type=MetapostTask, optional=False, description="")
        self._extractor.add_bool("dry", description="")
        self._extractor.set_group_name("Processing.Metapost")

    def get_arguments(self):
        super().get_arguments()
        self._task = self._extractor.get_value("task")
        self._dry = self._extractor.get_value("dry")

    def generate(self):
        self.extract()
        self.get_arguments()
        self._task.save_script()
        if not self._dry:
            self._task.start_metapost_with_script()
            self._task.post_run()

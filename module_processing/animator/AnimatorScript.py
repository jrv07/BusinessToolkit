from module_processing.PostProcessorScript import PostProcessorScript


class AnimatorPythonScript(PostProcessorScript):
    def __init__(self, script_file_name):
        super().__init__()
        self.file_name = script_file_name
        self._script_header.extend([
            "# python-script for animator",
            "# created by analysis-toolkit",
            "#",
            "from gnspy import a4",
            "modelView = a4.getViewByName('Model')",
            ""])
        self._script_footer.extend([
            "",
            "a4.executeCommand('bye')"])

    def add_command(self, command: str):
        self._instructions.append("a4.executeCommand('{}')".format(command))

    def add_commands(self, command_list: list):
        for command in command_list:
            self.add_command(command)


class AnimatorSessionFile(PostProcessorScript):
    def __init__(self, script_file_name):
        super().__init__()
        self.file_name = script_file_name
        self._script_header.extend([
            "$ session-file for animator",
            "$ created by analysis-toolkit",
            "$"
        ])
        self._script_footer.extend([
            "bye"
        ])

    def add_commands(self, instruction_list: list):
        self._instructions.extend(instruction_list)



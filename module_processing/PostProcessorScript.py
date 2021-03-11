import traceback
import logging


class PostProcessorScript:
    def __init__(self):
        self._instructions = []
        self._script_header = []
        self._script_footer = []
        self._script_file_name = ""

    def __str__(self):
        complete_script_lines = self.get_script_lines()
        return "\n".join(complete_script_lines)

    @property
    def file_name(self):
        return self._script_file_name

    @file_name.setter
    def file_name(self, value):
        self._script_file_name = value

    def add_command(self, instruction: str):
        self._instructions.append(instruction)

    def add_commands(self, command_list: list):
        raise NotImplementedError

    def save(self):
        script_content = str(self)
        try:
            with open(self._script_file_name, 'w') as file:
                file.write(script_content)
        except:
            logging.error(traceback.print_exc())

    def get_script_lines(self) -> list:
        complete_script_lines = []
        complete_script_lines.extend(self._script_header)
        complete_script_lines.extend(self._instructions)
        complete_script_lines.extend(self._script_footer)
        return complete_script_lines

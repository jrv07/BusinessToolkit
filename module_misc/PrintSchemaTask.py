import yaml
import json
from module_misc.BasicTask import BasicTask
import logging


class PrintSchemaTask(BasicTask):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._filename = None
        self._format = None
        self._extractor.add_str("filename", optional=False, description="")
        self._extractor.add_str("format", optional=False, default="json", valid_values=["json", "yaml"])
        self._extractor.set_group_name("Misc")

    def generate_schema(self):
        from instructions import instructions as main_instructions
        from module_misc.instructions import instructions as misc_instructions
        from module_pptx.instructions import instructions as pptx_instructions
        from module_processing.instructions import instructions as processing_instructions
        from module_input.instructions import instructions as input_instructions
        all_instructions = [
            *main_instructions,
            *misc_instructions,
            *pptx_instructions,
            *processing_instructions,
            *input_instructions
        ]

        descriptions = []
        for instruction in all_instructions:
            print(instruction.class_name)
            structure = instruction.get_structure()
            descriptions.append(structure)
        content = ""
        if self._format == "yaml":
            content = yaml.dump(descriptions)
        elif self._format == "json":
            content = json.dumps(descriptions, sort_keys=True, indent=4)
        try:
            from extra_functions import write_file
            write_file(self._filename, content)
        except Exception as exception:
            logging.error(exception)

    def get_arguments(self):
        super().get_arguments()
        self._filename = self._extractor.get_value("filename")
        self._format = self._extractor.get_value("format")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_schema()

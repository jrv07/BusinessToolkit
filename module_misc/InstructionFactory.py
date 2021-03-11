from module_misc.BasicTask import BasicTask


class InstructionFactory(BasicTask):
    def __init__(self, parameters, base_type, additional_constructor_arguments: list = None):
        super().__init__(parameters)
        self._extractor.set_exact_single_choice()
        self._instruction_input = None
        self._instruction_name = None
        self._instruction_input_type = None
        self._instruction: base_type = None
        self._additional_constructor_arguments = []
        if additional_constructor_arguments is not None:
            self._additional_constructor_arguments.extend(additional_constructor_arguments)

    @property
    def instruction(self):
        return self._instruction

    def get_arguments(self):
        super().get_arguments()
        self._instruction_name = self._extractor.single_name
        self._instruction_input = self._extractor.single_value
        self._instruction_input_type = self._extractor.single_value_type

    def generate_instruction(self, specific_additional_arguments: dict = None):
        args = [self._instruction_input]
        has_specific_arguments = False
        if specific_additional_arguments is not None:
            if self._instruction_name in specific_additional_arguments:
                has_specific_arguments = True
                args.extend(specific_additional_arguments[self._instruction_name])
        if not has_specific_arguments:
            args.extend(self._additional_constructor_arguments)
        self._instruction = self._instruction_input_type(*args)
        self._instruction.generate()

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()

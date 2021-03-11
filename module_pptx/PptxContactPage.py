from module_pptx.PptxPage import PptxPage
from module_pptx.PptxTextboxInstruction import PptxTextboxInstruction


class PptxContactPage(PptxPage):
    def __init__(self, parameters, presentation, settings=None):
        super().__init__(parameters, presentation, 2, settings)
        self._author = None
        self._function = None
        self._phone = None
        self._email = None
        self._extractor.add_str("author", optional=False, description="")
        self._extractor.add_str("function", optional=False, description="")
        self._extractor.add_str("phone", optional=False, description="")
        self._extractor.add_str("email", optional=False, description="")
        self._extractor.set_group_name("Presentation")

    def generate_contact_informations(self):
        contact_text_lines = [
            "{}".format(self._phone),
            "{}".format(self._email)
        ]
        instruction_input = {
            "placeholder": 10,
            "content": [
                {
                    "text": self._author + "\n",
                    "font": {
                        "font_bold": True
                    }
                },
                {
                    "text": self._function + "\n",
                },
                {
                    "text": "\n".join(contact_text_lines),
                    "font": {
                        "font_size": 10
                    }
                }
            ]
        }
        instruction = PptxTextboxInstruction(instruction_input, self._slide, self._settings)
        instruction.generate()
        self._instructions.append(instruction)

    def get_arguments(self):
        super().get_arguments()
        self._author = self._extractor.get_value("author")
        self._function = self._extractor.get_value("function")
        self._phone = self._extractor.get_value("phone")
        self._email = self._extractor.get_value("email")

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_contact_informations()

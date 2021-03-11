from pptx import Presentation
from module_pptx.PptxSlideCreationFactory import PptxSlideCreationFactory
from module_misc.BasicTask import BasicTask
import logging


class PptxPresentation(BasicTask):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._slides_input = None
        self._template = None
        self._presentation = None
        self._file_name = None
        self._extractor.add_list("slides", entry_type=dict, entry_object_type=PptxSlideCreationFactory,
                                 optional=False, description="")
        self._extractor.add_str("template", optional=False, description="")
        self._extractor.add_str("filename", optional=False, description="")
        self._extractor.set_group_name("Presentation")

    # def extract_pptx_slides(self):
    #     self._slides_input = extract_value_list("slides", self._parameters, entry_type=dict, optional=False)
    #
    # def extract_pptx_template(self):
    #     self._template = extract_value_str("template", self._parameters, optional=False)
    #
    # def extract_pptx_filename(self):
    #     self._file_name = extract_value_str("filename", self._parameters, optional=False)

    def start(self):
        self._presentation = Presentation(self._template)

    def finish(self):
        self._presentation.save(self._file_name)
        logging.info('Presentation "{}" successfully created'.format(self._file_name))

    def get_arguments(self):
        super().get_arguments()
        self._slides_input = self._extractor.get_value("slides")
        self._template = self._extractor.get_value("template")
        self._file_name = self._extractor.get_value("filename")

    def generate_presentation(self):
        self.start()
        for slide_input in self._slides_input:
            slide_instruction = PptxSlideCreationFactory(slide_input, self._presentation)
            slide_instruction.generate()
        self.finish()

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        # self.extract_pptx_slides()
        # self.extract_pptx_template()
        # self.extract_pptx_filename()
        self.generate_presentation()


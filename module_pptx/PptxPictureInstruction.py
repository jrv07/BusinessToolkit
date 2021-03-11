from module_pptx.PptxShapes import PptxShapeWithBorder
from module_misc.RegisterData import RegisterFile, RegisterPostProcessorWriteInstructionData


class PptxPictureInstruction(PptxShapeWithBorder):
    def __init__(self, parameters, slide, settings=None):
        super().__init__(parameters, slide, settings)
        self._picture_source = None
        self._extractor.add_source("picture_source_regfile", specifier="picture_source", source_type=RegisterFile,
                                   optional=False, alternative="picture_source_postprocessor", description="")
        self._extractor.add_source("picture_source_postprocessor", specifier="picture_source",
                                   source_type=RegisterPostProcessorWriteInstructionData, optional=False, description="")
        self._extractor.set_group_name("Presentation")

    def generate_picture(self):
        file_path = self._picture_source.file_path
        if self._height is not None:
            self._shape_object = self._slide.shapes.add_picture(file_path, self._left,
                                                                self._top, self._height, self._width)
        else:
            self._shape_object = self._slide.shapes.add_picture(file_path, self._left, self._top)

    def get_arguments(self):
        super().get_arguments()
        self._picture_source = self._extractor.get_value("picture_source_regfile")
        if self._picture_source is None:
            self._picture_source = self._extractor.get_value("picture_source_postprocessor")

    def generate(self):
        self.extract()
        self.get_arguments()
        super().generate()
        self.generate_picture()
        self.apply_styles()

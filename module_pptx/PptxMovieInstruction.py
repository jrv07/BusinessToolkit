from module_pptx.PptxShapes import PptxShapeWithBorder
from module_misc.RegisterData import RegisterFile, RegisterPostProcessorWriteInstructionData
import logging
import inspect


class PptxMovieInstruction(PptxShapeWithBorder):
    def __init__(self, parameters, slide, settings=None):
        super().__init__(parameters, slide, settings)
        self._movie_source: RegisterFile = None
        self._extractor.add_source("movie_source_regfile", specifier="movie_source", source_type=RegisterFile,
                                   optional=False, alternative="movie_source_postprocessor", description="")
        self._extractor.add_source("movie_source_postprocessor", specifier="movie_source",
                                   source_type=RegisterPostProcessorWriteInstructionData, optional=False, description="")

        # self._extractor.add_source("movie_source", source_type=RegisterFile, optional=False, description="")
        self._extractor.set_group_name("Presentation")

    def generate_movie(self):
        file_path = self._movie_source.file_path
        if self._height is None:
            logging.error('no "height" found in movie "{}"; parameters {}.'
                          .format(inspect.stack()[0][3], self._parameters))
            raise ValueError
        self._shape_object = self._slide.shapes.add_movie(file_path, self._left,
                                                          self._top, self._height, self._width)

    def get_arguments(self):
        super().get_arguments()
        self._movie_source = self._extractor.get_value("movie_source_regfile")
        if self._movie_source is None:
            self._movie_source = self._extractor.get_value("movie_source_postprocessor")

    def generate(self):
        self.extract()
        self.get_arguments()
        super().generate()
        self.generate_movie()
        self.apply_styles()

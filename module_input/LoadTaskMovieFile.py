from module_input.LoadTaskFileCopy import LoadTaskFileCopy


class LoadTaskMovieFile(LoadTaskFileCopy):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)

    def generate_import_movie(self):
        from share_objects import moviesDir
        self.generate_import_file(moviesDir)

    def generate(self):
        self.extract()
        self.get_arguments()
        super().generate()
        self.generate_import_movie()


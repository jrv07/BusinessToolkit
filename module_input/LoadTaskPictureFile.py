from module_input.LoadTaskFileCopy import LoadTaskFileCopy


class LoadTaskPictureFile(LoadTaskFileCopy):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)

    def generate_import_picture(self):
        from share_objects import picturesDir
        self.generate_import_file(picturesDir)

    def generate(self):
        self.extract()
        self.get_arguments()
        super().generate()
        self.generate_import_picture()


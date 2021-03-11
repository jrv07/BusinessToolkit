from module_misc.WithStoreData import WithStoreData
import random


class ComputeTableData(WithStoreData):
    def __init__(self, parameters, settings=None):
        super().__init__(parameters, settings)
        self._example_table_data = None
        self._type = None
        self._extractor.add_str("type", valid_values=["sid2s", "big_random", "side_crash"], optional=False,
                                description="")
        self._extractor.set_group_name("Misc")

    def generate_sid2s_data(self):
        self._example_table_data = [
            ["", "Target", "01V015", "06B004"],
            ["SID2s Rear Shoulder", 8.5, 8.51, 8.05],
            ["SID2s Rear Thorax", 8.0, 3.68, 4.72],
            ["SID2s Rear Pelvis", 9.0, 7.81, 8.88],
        ]

    def generate_big_random_data(self):
        data_table = []
        cols = 20
        rows = 28
        first_row = [""]
        for col_ind in range(cols):
            first_row.append("Sp {}".format(col_ind + 1))
        data_table.append(first_row)
        for row_ind in range(rows):
            data_row = ["Zeile {}".format(row_ind + 1)]
            for col_ind in range(cols):
                data_row.append(random.uniform(0, 100))
            data_table.append(data_row)
        self._example_table_data = data_table

    def generate_side_crash_data(self):
        data_table = [
            ['', 'HIC 15ms', 'Halsdehnung posFz kN', 'Halsdehnung negFz kN', 'Schulter s mm', 'Rippe oben s mm',
             'Rippe mitte s mm', 'Rippe unten s mm', 'Abdomen oben s mm', 'Abdomen unten s mm',
             'Average Rippe 1 5 s mm', 'Worst Case Rippe 1 5 s mm', 'Worst Case Rippe deflection rate 1 5 m s',
             'Worst Case Rippe VC 1 5 m s', 'Iliac F kN', 'Acetabulum F kN', 'I A C F kN'],
            ['Zielwerte', 560.7, 1.89, 2.25, 54, 30.6, 30.6, 30.6, 30.6, 30.6, 30.6, 45.9, 7.38, 0.9, 3.6, 3.6, 4.59],
            ['Gesetzeswerte', 623, 2.1, 2.5, 60, 34, 34, 34, 34, 34, 34, 51, 8.2, 1, 4, 4, 5.1],
            ['S00EG008_TRW26_1x21', 40, 0.9, 0.08, 19.8, 30.3, 36.6, 40.7, 38.8, 36.7, 36.6, 40.7, 5.19, 0.93, 1.44, 0.76, 2.08],
            ['S00EG008_TRW26_1x25', 38, 1, 0.06, 22.6, 27.8, 33.8, 38.9, 37.1, 35.3, 34.6, 38.9, 4.89, 0.82, 1.43, 0.71, 1.98],
            ['S00EG008_TRW26_1x29', 36, 0.94, 0.07, 23, 27.4, 32.3, 36.5, 35, 33.4, 32.9, 36.5, 4.55, 0.73, 1.28, 0.75, 1.87],
            ['S00EG035a_TRW54a_1x25', 52, 1.11, 0.05, 20.5, 30.7, 36.7, 41, 38.3, 34.8, 36.3, 41, 4.57, 0.87, 1.42, 0.97, 2.34],
            ['G01CS4315', 138, 0.92, 0.17, 31.7, 37.7, 44.8, 43.5, 38.6, 35.1, 39.9, 44.8, 4.28, 0.96, 1.3, 1.27, 2.45]
        ]
        self._example_table_data = data_table

    def generate_example_table_data(self):
        if self._type == "sid2s":
            self.generate_sid2s_data()
        elif self._type == "big_random":
            self.generate_big_random_data()
        elif self._type == "side_crash":
            self.generate_side_crash_data()

    def generate_store_data(self):
        self._store_data = self._example_table_data

    def get_arguments(self):
        super().get_arguments()
        self._type = self._extractor.get_value("type")

    def generate(self):
        self.extract()
        self.get_arguments()
        super().generate()
        self.generate_example_table_data()
        self.generate_store_data()
        self.store_in_register()

from module_misc.ConfigurationVariable import ConfigurationVariable
from module_misc.ConfigurationOptions import ConfigurationOptions
from module_misc.InstructionFactory import InstructionFactory
from module_misc.BasicTask import BasicTask
from module_input.LoadTaskCurves import LoadTaskCurves
from module_input.LoadTaskPictureFile import LoadTaskPictureFile
from module_input.LoadTaskMovieFile import LoadTaskMovieFile
from module_processing.arrk.Plot.CurvePlot import CurvePlot
from module_processing.arrk.Calculator.CurveCalculator import CurveCalculator
from module_misc.DefineVariable import DefineVariable
from module_misc.PrintSchemaTask import PrintSchemaTask
from module_pptx.PptxPresentation import PptxPresentation
from module_processing.animator.AnimatorTask import AnimatorTask, AnimatorRun
from module_processing.metapost.MetapostTask import MetapostTask, MetapostRun
from module_misc.ComputeTableData import ComputeTableData
from module_misc.ConfigurationVariables import ConfigurationVariables
import logging
import yaml
import copy


class ModuleTaskInstructionData:
    def __init__(self, instruction_type, description):
        self._instruction_type = instruction_type
        self._description = description

    @property
    def instruction_type(self):
        return self._instruction_type

    @property
    def description(self):
        return self._description


class IncludeModuleTasksTask(BasicTask):
    def __init__(self, parameters, settings=None, variables: ConfigurationVariables = None):
        super().__init__(parameters, settings)
        self._variables = variables
        self._file_path = None
        self._extractor.add_str("file_path", optional=False, description="")
        self._extractor.set_name("Include")
        self._extractor.set_group_name("Misc")

    def parse_include(self):
        with open(self._file_path, 'r') as f:
            content = f.read() + "\n"
            return yaml.load(content, Loader=yaml.FullLoader)

    def get_arguments(self):
        super().get_arguments()
        self._file_path = self._extractor.get_value("file_path")

    def generate_include_configuration(self):
        include_parameters = self.parse_include()
        include_configuration = Configuration(include_parameters, options=None, variables=self._variables)
        include_configuration.generate()

    def generate(self):
        super().generate()
        self.extract()
        self.get_arguments()
        self.generate_include_configuration()


class ModuleTaskFactory(InstructionFactory):
    def __init__(self, input_dict, variables: ConfigurationVariables = None):
        modules = {
            'data_load_curves': ModuleTaskInstructionData(LoadTaskCurves, ""),
            'data_plot': ModuleTaskInstructionData(CurvePlot, ""),
            'data_load_picture': ModuleTaskInstructionData(LoadTaskPictureFile, ""),
            'data_load_movie': ModuleTaskInstructionData(LoadTaskMovieFile, ""),
            'curves_calculation': ModuleTaskInstructionData(CurveCalculator, ""),
            'print_schema': ModuleTaskInstructionData(PrintSchemaTask, ""),
            'define_variable': ModuleTaskInstructionData(DefineVariable, ""),
            "pptx_task": ModuleTaskInstructionData(PptxPresentation, ""),
            'animator_task': ModuleTaskInstructionData(AnimatorTask, ""),
            'animator_run': ModuleTaskInstructionData(AnimatorRun, ""),
            'metapost_task': ModuleTaskInstructionData(MetapostTask, ""),
            'metapost_run': ModuleTaskInstructionData(MetapostRun, ""),
            'compute_table_data': ModuleTaskInstructionData(ComputeTableData, ""),
            'include': ModuleTaskInstructionData(IncludeModuleTasksTask, ""),
        }
        self._variables = self.get_variables(variables)
        settings = self.get_settings(input_dict, modules)
        parameters = self.get_parameters(input_dict, settings)
        super().__init__(parameters, BasicTask, additional_constructor_arguments=[settings])
        for module_name, module_data in modules.items():
            self._extractor.add_object(module_name, module_data.instruction_type, description=module_data.description)
        self._extractor.set_name("Task")
        self._extractor.set_group_name("Misc")

    @staticmethod
    def get_variables(variables):
        if variables is None:
            return ConfigurationVariables()
        else:
            return copy.copy(variables)

    @staticmethod
    def get_settings(input_dict, modules):
        settings = dict(input_dict)
        for module_name in modules.keys():
            if module_name in settings:
                settings.pop(module_name)
        return settings

    def get_parameters(self, input_dict, settings):
        parameters = dict(input_dict)
        for settings_key in settings.keys():
            parameters.pop(settings_key)
        self._variables.replace_jinja_variables_dictionary(parameters)
        return parameters

    def generate(self):
        super().generate()
        task_type_name = self._extractor.single_value_type.__name__
        logging.info("Started Module Task of Type: {}".format(task_type_name))
        specific_additional_constructor_arguments = {
            "include": [self._settings, self._variables]
        }
        self.generate_instruction(specific_additional_constructor_arguments)
        logging.info("Task finished ({})".format(task_type_name))


class Configuration(BasicTask):
    def __init__(self, parameters, options: ConfigurationOptions = None, variables: ConfigurationVariables = None):
        super().__init__(parameters)
        self._options: ConfigurationOptions = options
        self._tasks_input = None
        if variables is None:
            self._variables = ConfigurationVariables()
        else:
            self._variables = copy.copy(variables)
        self._extractor.add_list("tasks", entry_type=dict, entry_object_type=ModuleTaskFactory, optional=False,
                                 description="")
        self._extractor.add_list("vars", entry_type=dict, entry_object_type=ConfigurationVariable, description="")
        self._extractor.set_main()
        self._extractor.set_name("Yaml")
        self._extractor.set_group_name("Main")

    def get_tasks(self):
        self._tasks_input = self._extractor.get_value("tasks")

    def get_variables(self):
        variables_input = self._extractor.get_value("vars")
        if variables_input is not None:
            for variable_input in variables_input:
                variable = ConfigurationVariable(variable_input)
                variable.generate()
                self._variables.add_variable(variable.data)

    def get_arguments(self):
        super().get_arguments()
        self.get_tasks()
        self.get_variables()

    def run(self):
        if self._tasks_input is not None:
            for task_input in self._tasks_input:
                task = ModuleTaskFactory(task_input, variables=self._variables)
                task.generate()

    def generate(self):
        self.extract()
        self.get_arguments()
        self.run()

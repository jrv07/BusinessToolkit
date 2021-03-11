from module_misc.ConfigurationVariable import ConfigurationVariableData
from typing import List
import logging
import jinja2
import copy


class ConfigurationVariables:
    def __init__(self):
        self._variables: List[ConfigurationVariableData] = []

    def __copy__(self):
        new_configuration_variables = ConfigurationVariables()
        for variable in self._variables:
            new_configuration_variables.add_variable(copy.copy(variable))
        return new_configuration_variables

    @property
    def as_dictionary(self):
        output = {}
        for variable in self._variables:
            output.update({
                variable.name: variable.value
            })
        return output

    @property
    def count(self):
        return len(self._variables)

    def parse_variable(self, new_variable: ConfigurationVariableData):
        if self.count > 0:
            template_environment = jinja2.Environment(undefined=jinja2.make_logging_undefined())
            try:
                parsed_value = template_environment.from_string(str(new_variable.value)).render(self.as_dictionary)
                new_variable.value = parsed_value
                return new_variable
            except Exception as exception:
                logging.error('when processing variable "{}" (value {}) using jinja2'
                              .format(new_variable.name, new_variable.value))
                logging.error(exception)
        return new_variable

    def add_variable(self, new_variable: ConfigurationVariableData):
        parsed_variable = self.parse_variable(new_variable)
        found = False
        for index, variable in enumerate(self._variables):
            if variable.name == new_variable.name:
                logging.info(f'Variable "{variable.name}" has already been defined and will be overwritten! '
                             f'Stored value so far: "{variable.value}"; '
                             f'new value "{new_variable.value}"')

                self._variables[index].value = parsed_variable.value
                found = True
                break
        if not found:
            self._variables.append(parsed_variable)

    def replace_jinja_variables_dictionary(self, parameters: dict):
        for field_name, value in parameters.items():
            if isinstance(value, str):
                parameters[field_name] = self.replace_jinja_variables_string(field_name, value)
            elif isinstance(value, list):
                for element_index, element_value in enumerate(value):
                    if isinstance(element_value, str):
                        value[element_index] = self.replace_jinja_variables_string("in list: " + field_name,
                                                                                   element_value)
                    elif isinstance(element_value, dict):
                        self.replace_jinja_variables_dictionary(value[element_index])
            elif isinstance(value, dict):
                # local_vars = self._variables.copy()
                # if 'vars' in value:
                #     local_vars.update(value['vars'])
                # dictionary_nested = value
                self.replace_jinja_variables_dictionary(value)

    def replace_jinja_variables_string(self, field_name, field_content):
        parsed_content = field_content
        template_environment = jinja2.Environment(undefined=jinja2.make_logging_undefined())
        try:
            parsed_content = template_environment.from_string(str(field_content)).render(self.as_dictionary)
            # logging.info('string "{}" into "{}" using jinja'.format(stringToReplace, stringReplaced))
        except Exception as exception:
            logging.error('when processing variable "%s" (value %s) using jinja2' % (field_name, field_content))
            logging.error(exception)
        return parsed_content

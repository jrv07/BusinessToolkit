# import unittest
# import os,sys,inspect
# import time
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)
# import task
#
# import pytest
#
# class TestModuleTask(unittest.TestCase):
#   """
#   Test methods of class Block, ModuleTask (sub-classes of _Task)
#   """
#   def test_module_task_class_block_init(self):
#     '''
#     Test initialization and variable process
#     '''
#     blockObject = task.Block({},
#                                 task.Options(),
#                                  {'var1': 'hi', 'var2': '{{ var1 }} everyone', 'var3': 'Guten Tag',
#                                   'foo': "{{ var2 }}, what's up; {{ var3 }}"})
#     self.assertEqual(blockObject.variables, {'var1': 'hi', 'var2': 'hi everyone', 'var3': 'Guten Tag',
#                                             'foo': "hi everyone, what's up; Guten Tag"})
#
#   def test_module_task_class_block_init_warning(self):
#     '''
#     Test initialization and variable process
#     '''
#     with self.assertLogs() as logs:
#       blockObject = task.Block({},
#                                    task.Options(),
#                                    {'var1': 'hi', 'var4': '{{ var2 }} Hallo {{ var3 }}'})
#     self.assertEqual(logs.output, ['WARNING:jinja2.runtime:Template variable warning: var2 is undefined',
#                                    'WARNING:jinja2.runtime:Template variable warning: var3 is undefined'])
#
#   def test_module_task_class_moduletask_process_print(self):
#     '''
#     Test module print
#     '''
#     taskObject = task.ModuleTask({'name': 'print task', 'print': 'print output: foo = {{ foo }}'},
#                                 task.Options(),
#                                  {'foo': "value for replacement"})
#     self.assertEqual(taskObject.process(), "print output: foo = value for replacement")
#
#
#   def test_module_task_class_moduletask_process_dummy_error(self):
#     '''
#     Test exception using a dummy module
#     '''
#     with self.assertRaises(SystemExit) as cm:
#       taskObject = task.ModuleTask({'name': 'dummy task', 'dummy': 'execute dummy task'},
#                                     task.Options(), {})
#       taskObject.process()
#     self.assertEqual(cm.exception.code, 2)
#
#
#   def test_module_task_fragments_include(self):
#     '''
#     Test fragments & include
#     '''
#     import platform
#     currentPlatform = platform.system()
#     separator = '/'
#     if currentPlatform == 'Windows':
#       separator = '\\'
#     import os
#     script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
#     rel_path01 = "use-cases" + separator + "tasks.yaml"
#     abs_file_path01 = os.path.join(script_dir, rel_path01)
#     rel_path02 = "use-cases" + separator + "tasks2.yaml"
#     abs_file_path02 = os.path.join(script_dir, rel_path02)
#     file01 = abs_file_path01
#     file02 = abs_file_path02
#     settings = {'vars': {'var1': 'hi', 'var2': '{{ var1 }} everyone', 'var3': 'Guten Tag',
#                          'var4': "{{ var2 }}, what's up; {{ var3 }}"},
#                 'fragments': [{'name': 'fragment 01',
#                                'block': [{'name': 'print task', 'print_warning': 'print output1: {{ var1 }}'},
#                                          {'name': 'additional task', 'print_warning': 'additional task'}]},
#                               {'name': 'fragment 02', 'include': file01}],
#                 'tasks': [{'name': 'print task4', 'print_warning': 'print output4: {{ var3 }}'},
#                           {'name': 'use fragment 02', 'use': 'fragment 02'}, {'include': file02},
#                           {'name': 'use fragment 01', 'use': 'fragment 01'}]}
#     with self.assertLogs() as logs:
#       task.run_task(settings, task.Options(), {})
#     self.assertEqual(logs.output, [ 'WARNING:root:print output4: Guten Tag',
#                                     'WARNING:root:print output2: hi everyone',
#                                     "WARNING:root:print output3: hi everyone, what's up; Guten Tag",
#                                     'WARNING:root:print output5: hi everyone hi',
#                                     "WARNING:root:print output6: hi everyone, what's up; Guten Tag hi",
#                                     'WARNING:root:print output1: hi',
#                                     'WARNING:root:additional task'])
#
#
#   def test_module_task_identify_unknown_fields(self):
#     '''
#     Test fragments, include, unknown fields
#     '''
#     settings = {'vars': {'var1': 'hi', 'var2': '{{ var1 }} everyone', 'var3': 'Guten Tag',
#                          'var4': "{{ var2 }}, what's up; {{ var3 }}"},
#                 'fragments': [{'name': 'fragment 01', 'dummy': 'dummy-field',
#                                'block': [{'name': 'print task', 'print': 'print output1: {{ var1 }}'},
#                                          {'name': 'additional task', 'print': 'additional task'}]},
#                               {'name': 'fragment 02', 'block': [{'name': 'print task2',
#                                                                  'print': "print output2: {{ var2 }}"},
#                                                                 {'name': 'print task3',
#                                                                  'print': "print output3: {{ var4 }}"}],
#                                'extra': 'extra'}],
#                 'tasks': [{'name': 'print task4', 'dummy2': 'dummy_field_02', 'extra_field': 'extra value',
#                            'print': 'print output4: {{ var3 }}'},
#                           {'name': 'use fragment 02', 'add_filed': 'add_field', 'use': 'fragment 02'},
#                           {'block': [{'name': 'print task2', 'print': "print output5: {{ var2 }} {{ var1 }}"},
#                                      {'name': 'print task3', 'print': "print output6: {{ var4 }} {{ var1 }}"}],
#                            'dummy03': 'dummy_value03'},
#                           {'name': 'use fragment 01', 'use': 'fragment 01'}],
#                 'dummy_task': {'something': 'anything'}}
#     with self.assertLogs() as logs:
#       task.run_task(settings, task.Options(), {})
#     self.assertEqual(logs.output, [ "WARNING:root:Following fields are unknown and will not be processed: "
#                                     "{'dummy_task': {'something': 'anything'}}",
#                                     "WARNING:root:Following fields are unknown and will not be processed: "
#                                     "{'dummy2': 'dummy_field_02', 'extra_field': 'extra value'}",
#                                     'INFO:root:print output4: Guten Tag',
#                                     "WARNING:root:Following fields are unknown and will not be processed: "
#                                     "{'add_filed': 'add_field'}",
#                                     "WARNING:root:Following fields are unknown and will not be processed: "
#                                     "{'extra': 'extra'}",
#                                     'INFO:root:print output2: hi everyone',
#                                     "INFO:root:print output3: hi everyone, what's up; Guten Tag",
#                                     "WARNING:root:Following fields are unknown and will not be processed: "
#                                     "{'dummy03': 'dummy_value03'}",
#                                     'INFO:root:print output5: hi everyone hi',
#                                     "INFO:root:print output6: hi everyone, what's up; Guten Tag hi",
#                                     "WARNING:root:Following fields are unknown and will not be processed: "
#                                     "{'dummy': 'dummy-field'}",
#                                     'INFO:root:print output1: hi',
#                                     'INFO:root:additional task'])
#
#   def test_module_task_multiple_variable_definition(self):
#     '''
#     Test fragments, include, unknown fields
#     '''
#     settings = {'vars': {'var1': 'hi', 'var3': '{{ var1 }} Guten Tag',
#                          'var5': '{{ var3 }}, to be used inside fragment 01'},
#                 'fragments': [{'name': 'fragment 01', 'vars': {'var_1': '{{ var1 }} --', 'var_2': '{{ var3 }} **'},
#                                'block': [{'name': 'print task', 'print': 'print output1: {{ var_1 }}'},
#                                          {'name': 'additional task',
#                                           'print': 'additional task {{ var_print }}; {{ variable01 }}',
#                                           'vars': {'var_print': '{{ var_1 }} {{ var_2 }}'}}]}],
#                 'tasks': [{'name': 'print task4', 'vars': {'foo': '{{ var3 }}'}, 'print': 'print output4: {{ foo }}'},
#                           {'name': 'use fragment 01', 'use': 'fragment 01', 'vars': {'variable01': '{{ var5 }}'}}]}
#     with self.assertLogs() as logs:
#       task.run_task(settings, task.Options(), {})
#     self.assertEqual(logs.output, ['INFO:root:print output4: hi Guten Tag',
#                                    'INFO:root:print output1: hi --',
#                                    'INFO:root:additional task hi -- hi Guten Tag **; '
#                                    'hi Guten Tag, to be used inside fragment 01'])
#
#   def test_module_task_duplicate_variables(self):
#     '''
#     Test errors for duplicate variables.
#     In the following example variable03 is defined twice, but in parallel --> t should nor raise any error!
#     '''
#     settings = {'vars': {'multiple_variable': 'first value', 'variable02': '1st Value'},
#                 'fragments': [{'name': 'fragment 01', 'vars': {'multiple_variable': 'third value',
#                                                                'variable02': '3rd Value'},
#                                'block': [{'name': 'print task', 'print': '- {{ multiple_variable }} -'},
#                                          {'name': 'additional task',
#                                           'print': '{{ multiple_variable }}; {{ multiple_variable }}'},
#                                          {'name': 'print task2', 'vars': {'multiple_variable': "fourth value",
#                                                                           'variable02': "4th Value"},
#                                           'print': "{{ multiple_variable }} -- {{ variable02 }}"}]}],
#                 'tasks': [{'name': 'use fragment 01', 'use': 'fragment 01',
#                            'vars': {'multiple_variable': 'second value', 'variable02': '2nd Value',
#                                     'variable03': 'definition under fragment'}},
#                           {'name': 'final task', 'print': '{{ variable03 }}',
#                            'vars': {'variable03': 'definition for final task'}}]}
#
# if __name__ == '__main__':
#   unittest.main()

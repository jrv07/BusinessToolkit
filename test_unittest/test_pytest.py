# import pytest
# import os,sys,inspect
# #import time
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)
# import task
#
# #class TestClass(object):
# def test_when_sinlge():
#   '''
#       Test when single
#   '''
#   taskObject = task.ModuleTask({'name': 'final task', 'when': 'color == "red"', 'vars': {'variable01': 'Hi there!'},
#                                 'print': '{{ variable01 }}'},
#                                task.Options(),
#                                {'color': 'red'})
#   assert taskObject.run() == 'Hi there!'
#
# def test_when_sinlge_no_ouput():
#   '''
#       Test when single
#   '''
#   taskObject = task.ModuleTask({'name': 'final task', 'when': 'color == "red"', 'vars': {'variable01': 'Hi there!'},
#                                 'print': '{{ variable01 }}'},
#                                task.Options(),
#                                {'color': 'blue'})
#   assert taskObject.run() == None
#
# def test_loop_with_when_and_array_of_dict():
#   '''
#       Test loop with when and array of dict
#   '''
#   taskObject = task.ModuleTask({'name': 'task 1', 'loop': '{{ variants }}',
#                                 'when': 'item.color == "blue" or item.color == "green" or item.name == "variant 5"',
#                                 'print': ' {{ item.name }} in {{ item.color }}'},
#                                task.Options(),
#                                {'variants': [{'name': 'variant 1', 'color': 'blue'},
#                                              {'name': 'variant 2', 'color': 'red'},
#                                              {'name': 'variant 3', 'color': 'green'},
#                                              {'name': 'variant 4', 'color': 'black'},
#                                              {'name': 'variant 5', 'color': 'yellow'}]})
#   assert taskObject.run() == [' variant 1 in blue', ' variant 3 in green', ' variant 5 in yellow']
#
# def test_loop_with_array_and_control():
#   '''
#       Test loop with array and control with loop_var & index_var
#   '''
#   taskObject = task.ModuleTask({'name': 'task 1', 'loop': ['a', 'b', 'c', 'd'],
#                                 'loop_control': {'loop_var': 'label', 'index_var': 'position'},
#                                 'print': 'current-label {{ label }} in position {{ position }}'},
#                                task.Options(), {})
#   assert taskObject.run() == ['current-label a in position 0', 'current-label b in position 1',
#                               'current-label c in position 2', 'current-label d in position 3']
#
# def test_register():
#   #{'data_load_crv': {'filename': '3_curves.crv'}, 'register': 'curves_crv'}
#   import platform
#   currentPlatform = platform.system()
#   separator = '/'
#   if currentPlatform == 'Windows':
#     separator = '\\'
#   import os
#   script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
#   rel_path01 = "use-cases" + separator + "3_curves.crv"
#   abs_file_path01 = os.path.join(script_dir, rel_path01)
#   file01 = abs_file_path01
#
#   taskObject = task.ModuleTask({'data_load_crv': {'filename': file01}, 'register': 'curves_crv'},
#                                task.Options(), {})
#
#   import share_objects as share
#   assert taskObject.process() == share.register['curves_crv']
#   assert share.register['curves_crv'].filename == file01

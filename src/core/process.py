import os
import pathlib
import re
import sys
from . import linematches, convert
from . import errors

class Program:
    def __init__(self, file, auto_run=True) -> None:
        
        self.auto_run = auto_run

        self.__modernbinary_path = str(pathlib.Path(__file__).resolve().parent)

        self.__userpath = os.getcwd()

        self.collecting_condition = False

        self.functions = {}

        self.data = []

        self.process_cache = []

        self.variables = {}

        self.exec_loc = {}

        self.imported_modules = []

        self.add_to_output = ''
        
        if auto_run:
            with open(file, 'r+') as main:
                self.data = main.read().splitlines()
                del main
            
            self.line_on_check = 0

            while self.line_on_check < len(self.data):
                line = self.data[self.line_on_check]
                r = self.run_line(line)
                self.line_on_check += 1
                if r:
                    errors_list = {cl:eval('errors.'+cl) for cl in dir(errors)}
                    if r in [j for i,j in errors_list.items()]:
                        print('['+str(
                            [i for i,j in errors_list.items()][list(errors_list.values()).index(r)]
                        )+'] on line '+str(self.data.index(line)+1))
                        if self.auto_run:
                            sys.exit(1)
            print()

    def run_line(self, line):
            line = self.comment_checkup(line)
            if not line:
                return
            to_return = self.command_regex_search(line)
            if not self.auto_run:
                self.data.append(line)
            return to_return

    def comment_checkup(self, line):
        if(line.rstrip() == ''):
            return
        if(line.startswith('#')):
            return
        elif('#' in line):
            return line.split('#')[0].rstrip()
        return line

    def define(self, key, value):
        self.variables[convert.totext(key)] = convert.totext(value)

    def add_to_modernbinary(self, mb_format, add=''):
        return convert.tomb(
            convert.totext(mb_format)+add
        )

    def is_module_exist(self, module_name):
        module_name = convert.totext(module_name)
        for r, d, f in os.walk(os.path.join(self.__modernbinary_path, '..', 'libs')):
            for module in f:
                if module.lower() == (module_name+'.mb').lower():
                    return {
                        'result': True,
                        'type': 'built-in',
                        'path': os.path.join(r, module)
                    }
        for r, d, f in os.walk(os.path.join(self.__userpath)):
            for module in f:
                if module.lower() == (module_name+'.mb').lower():
                    return {
                        'result': True,
                        'type': 'file',
                        'path': os.path.join(r, module)
                    }
        return {
            'result': False
        }

    def import_module(self, module_name):
        load_module = self.is_module_exist(module_name)
        if not load_module['result']:
            return errors.ModuleDoesNotExist
        self.imported_modules.append(load_module)
        return load_module

    def strip_list(self, _list):
        for i, v in enumerate(_list):
            if(type(v) == str):
                _list[i] = str(v).rstrip().lstrip()
        return _list

    def command_regex_search(self, line):
    
        if not re.search('\\(([^)]+)\\)', line):
            return

        if line == '':
            line = ' '

        elif(line.endswith('::()')):
            line = line.replace('::()' , '')
            self.add_to_output += '\\n'

        elif(line.endswith(':()')):
            line = line.replace(':()', '')
            self.add_to_output += ' '

        matches = re.findall('\\(([^)]+)\\)', line)
        for index, m in enumerate(matches):
            matches[index] = m.rstrip().lstrip()
        del m

        if(matches[0].startswith('[') and matches[0].endswith(']')):
            try:
                function_commands = self.functions[
                    convert.totext(matches[0].replace('[', '').replace(']', ''))
                ]
                for function_line in function_commands[::-1]:
                    self.data.insert(
                        self.line_on_check+1,
                        function_line
                    )
                return
            except:
                return errors.MBSyntaxError

        if matches[0] == '43':
            _import = self.import_module(matches[1])
            if _import == errors.ModuleDoesNotExist:
                return errors.ModuleImportError
            with open(_import['path'], 'r+') as module_data:
                module_data = module_data.read()
            after_import_index = self.data.index(line)+1
            for line in module_data.splitlines()[::-1]:
                self.data.insert(
                    after_import_index,
                    line
                )
            return

        if '118:' in matches[0]:
            to_define = matches[1]
            if re.search('\[(.*?:.*?)\]', matches[1]):
                matches_in_var = re.findall('\[(.*?:.*?)\]', matches[1])[0].split(':')
                to_define = self.command_regex_search('({})=({})'.format(
                    str(matches_in_var[0]).lstrip().rstrip(),
                    str(matches_in_var[1]).lstrip().rstrip()
                ))
                to_define = ' ' if to_define == '' else to_define
                to_define = convert.tomb(to_define)
            return self.define(
                matches[0].split(':(')[-1].rstrip().lstrip(),
                to_define.lstrip().rstrip()
            )
        
        # Start Condition Checking

        if('105 204:(' in matches[0]):
            condition = matches[0].split(':(')[1]
            is_true, condition_op = False, ''
            for op in linematches.OPERATORS:
                if op in condition:
                    is_true = True
                    condition_op = op
                    continue
            if not is_true:
                return errors.MBSyntaxError
            condition_split = self.strip_list(condition.split(condition_op))
            
            cond_to_eval = []

            for obj in condition_split:
                if obj.startswith('[[') and obj.endswith(']]'):
                    cvt = convert.totext(str(obj.replace('[[', '').replace(']]', '').rstrip().lstrip()))
                    if(cvt in self.variables):
                        cond_to_eval.append('"{}"'.format(self.variables[cvt]))
                    else:
                        return errors.UnDefineError
                else:
                    return errors.ConditionError
            condition_lines = []
            self.line_on_check += 1
            try:
                while self.data[self.line_on_check].rstrip().lstrip() != '}':
                    condition_lines.append(self.data[self.line_on_check].rstrip().lstrip())
                    self.line_on_check += 1
            except:
                return errors.MBSyntaxError
            if eval(condition_op.join(cond_to_eval)):
                for condition_line in condition_lines[::-1]:
                    self.data.insert(
                        self.line_on_check+1,
                        condition_line
                    )
            return

        # Start Function Checking
        if '102:' in matches[0]:
            if line.endswith('{'):
                self.functions[convert.totext(matches[0].split(':(')[1])] = []
                function_lines = []
                self.line_on_check += 1
                try:
                    while self.data[self.line_on_check].rstrip().lstrip() != '}':
                        function_lines.append(self.data[self.line_on_check].rstrip().lstrip())
                        self.line_on_check += 1
                except:
                    return errors.MBSyntaxError
                self.functions[
                    convert.totext(matches[0].split(':(')[1])
                ] = function_lines
                return

        stripped_firstmatch = matches[1].rstrip().lstrip()
        if stripped_firstmatch.startswith('[[') and stripped_firstmatch.endswith(']]'):
            matches_cache = matches[1].rstrip().lstrip()
            matches[1] = convert.tomb(self.variables[convert.totext(
                stripped_firstmatch.replace(']]', '').replace('[[', '').rstrip().lstrip()
            )])
            line = line.replace(matches_cache, matches[1])

        code_info = linematches.get(matches[0])
        if not code_info:
            return errors.UnknownCommand
        
        returnval = ''
        exec('returnval = {}({}+"{}")'.format(
            code_info['c'],
            ', '.join(
                [
                    '"{}"'.format(i) for i in list([convert.totext(i) for i in [matches[int(i)] for i in code_info['argsfrommatches']]]+
                    code_info['argvs']) # Custom argvs
                ]+['{}={}'.format(i,j) for i,j in code_info['kwargs'].items()]
            ),
            self.add_to_output
        ), globals(), self.exec_loc)
        self.add_to_output = ''
        return self.exec_loc['returnval']
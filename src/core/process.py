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
                
            for line in self.data:
                self.run_line(line)

    def run_line(self, line):
        try:
            line = self.comment_checkup(line)
            if not line:
                return errors.NotLinePass
            to_return = self.command_regex_search(line)
            if not self.auto_run:
                self.data.append(line)
            return to_return
        except:
            return errors.MBSyntaxError

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

    def command_regex_search(self, line):
        if not re.search('\\(([^)]+)\\)', line):
            return

        if line == '':
            line = ' '

        elif(line.endswith(':( )')):
            line = line.replace(':( )', '')
            self.add_to_output += ' '

        matches = re.findall('\\(([^)]+)\\)', line)
        for index, m in enumerate(matches):
            matches[index] = m.rstrip().lstrip()
        del m

        if matches[0] == '43':
            _import = self.import_module(matches[1])
            if _import == errors.ModuleDoesNotExist:
                print('[ImportError] Module does not exist on line '+str(
                    self.data.index(line)+1
                ))
                sys.exit(0)
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
                    str(matches_in_var[0]),
                    str(matches_in_var[1])
                ))
                to_define = ' ' if to_define == '' else to_define
                to_define = convert.tomb(to_define)
            return self.define(
                matches[0].split(':(')[-1],
                to_define
            )
        
        stripped_firstmatch = matches[1].rstrip().lstrip()
        if stripped_firstmatch.startswith('[[') and stripped_firstmatch.endswith(']]'):
            matches_cache = matches[1]
            matches[1] = convert.tomb(self.variables[convert.totext(
                stripped_firstmatch.replace(']]', '').replace('[[', '')
            )])
            line = line.replace(matches_cache, matches[1])

        code_info = linematches.get(matches[0])
        if not code_info:
            print('[UnknownCommand] Command code {} is not defined on line {}'.format(
                str(matches[0]),
                str(self.data.index(line)+1)
            ))
            if self.auto_run:
                sys.exit(1)
        
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
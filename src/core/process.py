import re
import sys
from . import linematches
from . import convert

class Program:
    def __init__(self, file) -> None:

        self.process_cache = []

        self.variables = {}

        self.exec_loc = {}

        self.add_to_output = ''

        with open(file, 'r+') as main:
            self.data = main.read().splitlines()
            del main
        
        for line in self.data:
            line = self.comment_checkup(line)
            if not line:
                continue
            self.command_regex_search(line)

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

    def command_regex_search(self, line):
        if not re.search('\\(([^)]+)\\)', line):
            return

        if line == '':
            line = ' '

        elif(line.endswith(':( )')):
            line = line.replace(':( )', '')
            self.add_to_output += ' '
        
        matches = re.findall('\\(([^)]+)\\)', line)

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
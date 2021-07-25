import re
import sys
from . import linematches
from . import convert

class Program:
    def __init__(self, file) -> None:

        self.process_cache = []

        self.variables = {}

        with open(file, 'r+') as main:
            self.data = main.read().splitlines()
            del main
        
        for line in self.data:
            try:
                line = self.comment_checkup(line)
                if not line:
                    continue
                self.command_regex_search(line)
            except:
                print('[SyntaxError] on line '+str(self.data.index(line)+1))
                print((' '*5)+'>> '+line)

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

    def command_regex_search(self, line):
        if re.search('\\(([^)]+)\\)', line):
            matches = re.findall('\\(([^)]+)\\)', line)

            if '118:' in matches[0]:
                return self.define(
                    matches[0].split(':(')[-1],
                    matches[1]
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
            

            exec('vrun = {}({})'.format(
                code_info['c'],
                ', '.join(
                    [
                        '"{}"'.format(i) for i in list([convert.totext(i) for i in [matches[int(i)] for i in code_info['argsfrommatches']]]+
                        code_info['argvs']) # Custom argvs
                    ]+['{}={}'.format(i,j) for i,j in code_info['kwargs'].items()]
                )
            ))
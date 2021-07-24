import re
import sys
from . import linematches
from . import convert

class Program:
    def __init__(self, file) -> None:

        self.process_cache = []

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

    def command_regex_search(self, line):
        if re.search('\\(([^)]+)\\)', line):
            matches = re.findall('\\(([^)]+)\\)', line)
            code_info = linematches.get(matches[0])
            if not code_info:
                print('[UnknownCommand] Command code {} is not defined on line {}'.format(
                    str(matches[0]),
                    str(self.data.index(line)+1)
                ))
                sys.exit(1)
            exec('{}({})'.format(
                code_info['c'],
                ', '.join(
                    [
                        '"{}"'.format(i) for i in list([convert.totext(i) for i in [matches[int(i)] for i in code_info['argsfrommatches']]]+
                        code_info['argvs']) # Custom argvs
                    ]+['{}={}'.format(i,j) for i,j in code_info['kwargs'].items()]
                )
            ))
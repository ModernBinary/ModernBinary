import sys
import core
from core import parser, convert, errors

class Shell(parser.Parser):
    def __init__(self) -> None:
        super().__init__(None, auto_run=False)

        print('ModernBinary Shell ['+core.__version__+'] activated.')

        while True:
            __input = input('>> ')
            if __input == convert.tomb('exit'):
                sys.exit(1)
            run = self.run_line(__input)
            if type(run) != type:
                if(run == errors.MBSyntaxError):
                    print('[Syntax Error]')
                    continue
                print()

try:
    shell = Shell()
except KeyboardInterrupt:
    sys.exit(1)

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
                errors_list = {cl:eval('errors.'+cl) for cl in dir(errors)}
                print(errors_list)
                if run in [j for i,j in errors_list.items()]:
                    print('['+str(
                        [i for i,j in errors_list.items()][list(errors_list.values()).index(run)]
                    )+'] on line '+str(self.data.index(__input)+1))
                    if self.auto_run:
                        sys.exit(1)

try:
    shell = Shell()
except KeyboardInterrupt:
    sys.exit(1)

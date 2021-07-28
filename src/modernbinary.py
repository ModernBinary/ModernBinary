import os
import sys
from core import convert, parser

def main():
    argv = sys.argv[1:]

    if not argv:
        print('[Error] You must enter the file name in the input arguments.')
        sys.exit(1)

    elif(argv[0] == '--texttomb'):
        print(convert.tomb(' '.join(argv[1:])))
        sys.exit(1)

    elif(argv[0] == '--mbtotext'):
        print(convert.totext(' '.join(argv[1:])))
        sys.exit(1)

    else:
        if not argv[0].endswith('.mb'):
            print('[Error] Your file format must be mb.')
            sys.exit(1)

        elif not os.path.isfile(argv[0]):
            print('[Error] There is no file named {}'.format(argv[0]))
            sys.exit(1)

        parser.Parser(argv[0])


if __name__ == '__main__':
    main()

import sys
from .lexer import Lexer
from .linematches import BASE
from .convert import tomb, totext
from .errors import (
    MBSyntaxError, ConditionError, ModuleDoesNotExist,
    ModuleImportError, UnDefineError, NotLinePass,
    UnknownCommand
)

class Parser:
    def __init__(self, file_name) -> None:

        self.DEBUG = False

        self.varcache = {}

        self.file_name = file_name
        with open(file_name, 'r+') as file:
            self.data = file.read()
        
        self.lexer = Lexer(self.data)

        for lex, argv in self.lexer.get_tokens():
            if 'errors.' in str(lex):
                lex.description = 'Invalid syntax : '+argv['char']
                self.show_error(lex, argv)
            try:
                r = self.basic_parse(lex)
                if self.DEBUG:
                    print(r)
                if 'errors.' in str(r):
                    self.show_error(r, lex)
                if not self.DEBUG:
                    exec(r)
            except Exception as e:
                raise e
                self.show_error(MBSyntaxError, lex)

    def show_error(self, error_class, lexer_object):
        text = '[ERROR] File "{}", line {}'.format(
            self.file_name,
            lexer_object['line']
        )
        if error_class == UnknownCommand:
            action = lexer_object['tokens'][0].split(':')[-1]
            error_class.description = action+' is not defined'
        text += '\n{}: {}'.format(
            str(error_class.__name__),
            error_class.description
        )
        print(text)
        sys.exit(1)

    def simple_parse_to_exec(self, token, lex):

        if 'var' in token:
            self.varcache[token['var']] = token['value']
            return ''

        if 'action' in token:
            loadbase = BASE[token['action']]
            push_in = ''
            finally_push_in = ''
            if 'call' in token:
                if 'value' in token:
                    finally_push_in += totext(token['value']).replace("\"", "\\\"")
                if token['call'] in self.varcache:
                    push_in = totext(self.varcache[token['call']]).replace("\"", "\\\"")
            else:
                push_in = totext(token['value']).replace("\"", "\\\"")

            push_in += finally_push_in

            return '{}({})'.format(
                loadbase['c'],
                '"{}"'.format(push_in)
            )
        

        return ''

    
    def basic_parse(self, lex):
        action = ''
        base_encode = {}
        if self.DEBUG:
            return lex
        for token in lex['tokens']:
            if token.startswith('ACTION:'):
                action = token.split('ACTION:')[-1]
                if action not in BASE:
                    return UnknownCommand
                base_encode['action'] = action
                continue

            if token.startswith('CALL:'):
                value = token.split(':')[-1]
                base_encode['call'] = value
                continue

            if token.startswith('VAR:'):
                var_name = token.split(':')[-1]
                base_encode['var'] = var_name
                continue

            if token.startswith('VAL:'):
                value = token.split('VAL:')[-1]
                base_encode['value'] = value
                continue


        if base_encode != {}:
            return self.simple_parse_to_exec(base_encode, lex)
        return ''
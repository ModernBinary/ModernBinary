import string
from os import error
import sys
from .lexer import Lexer
from .linematches import BASE, OPERATORS
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

        self.funccache = {}

        self.file_name = file_name
        with open(file_name, 'r+') as file:
            self.data = file.read()
        
        self.lexer = Lexer(self.data, file_name=self.file_name)

        self.run_lex(self.lexer.get_tokens())

    def run_lex(self, lex):
        for lex, argv in lex:
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
                error_class = MBSyntaxError
                error_class.description = 'unexpected EOF while parsing'
                self.show_error(error_class, lex)

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
        done = False
        error_class = MBSyntaxError

        if 'public_call' in token:
            if token['public_call'] in self.funccache:
                self.run_lex(self.funccache[token['public_call']])
            else:
                error_class = UnDefineError
                error_class.description = 'public name {} is not defined'.format(token['public_call'])
                self.show_error(error_class, lex)
            return ''

        if 'function' in token:
            lex_function = Lexer(token['codes'], '<function:{}>'.format(token['function'])).get_tokens()
            self.funccache[token['function']] = lex_function
            return ''
        
        if 'condition' in token:
            for condition_char in token['condition']:
                if condition_char in string.ascii_lowercase:
                    error_class = MBSyntaxError
                    error_class.description = 'unexpected EOF while parsing'
                    self.show_error(error_class, lex)

            for i in token['torun']:
                for op in OPERATORS:
                    if op in token['condition']:
                        done = True
                        break
                if not done:
                    try:
                        eval(str(token['condition']))
                    except:
                        error_class.description = 'Unknown operator used in condition : '+token['condition']
                        self.show_error(error_class, lex)
                if '[' in token['condition'] and ']' in token['condition']:
                    lex_condition = Lexer(token['condition'], lextype='condition', file_name=self.file_name).get_tokens()
                    for tok in lex_condition:
                        if tok.startswith('VAR'):
                            var = tok.split(':')[1]
                            if var in self.varcache:
                                token['condition'] = token['condition'].replace('[{}]'.format(var), self.varcache[var])
                            else:
                                error_class.description = 'Undefined variable used in condition : '+'[{}]'.format(var)
                                self.show_error(error_class, lex)
                if eval(token['condition']):
                    exec(self.basic_parse({'line': token['line'], 'pr_count': 0, 'tokens': i }))

        if 'var' in token:
            self.varcache[token['var']] = token['value']
            return ''

        if 'action' in token:
            loadbase = BASE[token['action']]
            push_in = ''
            finally_push_in = ''
            if 'call' in token:
                if 'value' in token:
                    if token['value']:
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
        collecting_if = collecting_func = 0
        base_encode = {}
        if self.DEBUG:
            return lex
        for token in lex['tokens']:

            if token == 'FUNC':
                collecting_func = 1
                continue

            if collecting_func:

                if collecting_func == 1:
                    base_encode['function'] = token
                    collecting_func = 2
                    continue

                elif collecting_func == 2:
                    collecting_func = 3
                    continue

                elif collecting_func == 3:
                    base_encode['codes'] = token
                    collecting_func = 4
                    continue

                elif collecting_func == 4:
                    collecting_func = 0
                    continue

            if token == 'IF':
                collecting_if = 1
                continue

            if collecting_if:
                base_encode['line'], base_encode['endline'] = lex['line'], lex['endline']
                if token == 'THEN':
                    continue

                if token == 'ENDIF' or collecting_if == 3:
                    collecting_if = 0
                    continue

                if collecting_if == 1:
                    base_encode['condition'] = token
                    collecting_if = 2
                    continue

                if collecting_if == 2:
                    base_encode['torun'] = token
                    collecting_if = 3
                    continue

            if token.startswith('ACTION:'):
                action = token.split(':')[-1].strip()
                if action not in BASE:
                    return UnknownCommand
                base_encode['action'] = action
                continue

            if token.startswith('CALL:'):
                value = token.split(':')[-1].strip()
                base_encode['call'] = value
                continue

            if token.startswith('PUBLIC_CALL:'):
                value = token.split(':')[-1].strip()
                base_encode['public_call'] = value
                continue
            
            if token.startswith('VAR:'):
                var_name = token.split(':')[-1].strip()
                base_encode['var'] = var_name
                continue

            if token.startswith('VAL:'):
                value = token.split('VAL:')[-1].strip()
                base_encode['value'] = value
                continue

        if base_encode != {}:
            return self.simple_parse_to_exec(base_encode, lex)
        return ''
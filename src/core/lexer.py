from os import error
import sys
import string
from core.linematches import OPERATORS
from core.errors import MBSyntaxError,UnknownCommand

class Lexer:
    def __init__(self, data, file_name='<stdin>', lextype='loadtoken') -> None:

        self.file_name = file_name

        self.lex_type = lextype

        self.data = data+('\n' if lextype != 'condition' else '')
        
        if lextype == 'loadtoken':
            self.TOKENS = self.Load_Tokens()
        elif lextype == 'condition':
            self.TOKENS = self.Load_Condition()
    
    def Load_Condition(self):
        TOKENS =  []
        cache = ''
        meta = {}
        for i in self.data:

            if cache in OPERATORS:
                TOKENS.append(cache)
                cache = ''
                continue

            if i == '[':
                meta['state'] = True
                cache = ''
                continue

            if i == ']':
                meta['state'] = False
                TOKENS.append('VAR:'+cache)
                cache = ''
                continue

            cache += i

        return TOKENS

    def Load_Tokens(self):
        TOKENS = []

        self.public_ind = -1

        def Reset():
            self.cache = ''

            self.is_first = True

            self.ind = -1

            self.is_more = False

            self.pr_count = 0

            self.collect_type = ''
            
            self.cr_count = 0

            self.cr_state = False

            self.pr_state = False

            self.line_cache = []

            self.if_statement = False

            self.condition = ''

            self.on_if = {}

            self.if_commands = False

        Reset()

        self.linenum = 1

        self.function_meta = {
            'open': False,
            'collect': False,
            'name': '',
            'state': False,
            'todo': '',
            'nocollect': 0
        }

        for char in self.data:
            self.ind += 1
            self.public_ind += 1

            if char == '[' and not self.function_meta['state']:
                if self.data[self.public_ind+1] == '*':
                    counter, call_object = 1, ''
                    while self.data[self.public_ind+counter] != ']':
                        counter += 1
                        if self.data[self.public_ind+counter] not in ['*', '[', ']']:
                            call_object += self.data[self.public_ind+counter]
                        if self.data[self.public_ind+counter] == '\n':
                            error_class = MBSyntaxError
                            error_class.description = 'unexpected EOF while parsing'
                            self.show_error(error_class, {'line': self.linenum, 'char': char})
                    else:
                        yield {
                            'line': self.linenum,
                            'pr_count': self.pr_count,
                            'tokens': ['PUBLIC_CALL:'+str(call_object)]
                        }, self.linenum
                    continue

            if char == '*':
                self.function_meta['open'] = True if not self.function_meta['open'] else False
                if not self.function_meta['open']:
                    self.function_meta['collect'] = True
                continue

            if self.function_meta['open']:
                self.function_meta['name'] += char
                continue

            if self.function_meta['collect']:

                if char in ['{', '}']:
                    if self.function_meta['state'] and char == '{':
                        self.function_meta['nocollect'] += 1
                        continue
                    if self.function_meta['state'] and char == '}':
                        if self.function_meta['nocollect'] >= 1:
                            self.function_meta['nocollect'] -= 1
                            continue
                    self.function_meta['state'] = True if not self.function_meta['state'] else False
                    if not self.function_meta['state']:
                        self.function_meta['collect'] = False
                        self.function_meta['open'] = False
                        self.function_meta['todo'] = self.function_meta['todo']
                        yield {
                            'line': self.linenum,
                            'pr_count': self.pr_count,
                            'tokens': ['FUNC', self.function_meta['name'], 'THEN', self.function_meta['todo'],'END']
                        }, self.linenum
                        self.function_meta['name'] = ''
                        self.function_meta['todo'] = ''
                    continue
                        
                if self.function_meta['state']:
                    self.function_meta['todo'] += char
                    continue

                continue

            if self.if_commands:
                if self.condition not in self.on_if:
                    self.on_if[self.condition] = ''
                if char != '}':
                    self.on_if[self.condition] += char
                else:
                    self.on_if[self.condition] = '\n'.join([i.strip() for i in self.on_if[self.condition].splitlines()])
                    complete = [i for i in Lexer(self.on_if[self.condition]).get_tokens(t='onlytoken')]
                    iftoks = ['IF', self.condition, 'THEN', complete, 'ENDIF']
                    TOKENS.append(iftoks)
                    yield {
                        'line': self.linenum,
                        'endline': self.linenum+self.on_if[self.condition].count('\n'),
                        'pr_count': self.pr_count,
                        'tokens': iftoks
                    }, self.linenum
                    self.if_commands = False
                    self.if_statement = False
                continue


            if self.if_statement:
                if char != '{':
                    self.condition += char.strip()
                else:
                    self.if_statement, self.if_commands = False, True
                continue

            if char in ['[', ']']:
                self.cr_state = True if char == '[' else False

                tag_name = 'VAL' if not self.pr_state else 'CALL'

                if self.is_more and not self.cache.startswith(tag_name+':'):
                    self.cache = tag_name+':'+self.cache

                if not self.cr_state:
                    if self.is_first:
                        self.is_first = False
                        self.cache = 'VAR:'+self.cache
                    self.line_cache.append(self.cache.strip())
                    self.cr_count += 1
                    self.collect_type = ''
                else:
                    self.collect_type = 'definevar'
                self.cache = ''
                continue

            if char in ['(', ')']:
                self.pr_state = True if char == '(' else False
                tag_name = 'VAL' if not self.cr_state else 'CALL'

                if self.is_more and not self.cache.startswith(tag_name+':') and self.cache:
                    self.cache = tag_name+':'+self.cache
                
                if not self.pr_state and self.cache:
                    if self.is_first:
                        self.is_first = False
                        self.cache = 'ACTION:'+self.cache
                    self.line_cache.append(self.cache.strip())
                    self.pr_count += 1
                    self.collect_type = ''
                else:
                    self.collect_type = 'runcommand'
                self.cache = ''
                continue

            if char == ":":
                if self.ind == 0:
                    self.if_statement = True
                continue

            if char == '=':
                self.is_more = True
                continue

            if char == '\n' or char == self.data[-1]:
                TOKENS.append(self.line_cache)

                yield {
                    'line': self.linenum,
                    'pr_count': self.pr_count,
                    'tokens': self.line_cache
                }, self.linenum

                Reset()
                self.linenum += 1
                continue

            if self.pr_state or self.cr_state:
                self.cache += char
                continue
            
            if char == ' ':
                continue

            error_class = MBSyntaxError
            error_class.description = 'Invalid syntax : \x1b[31m'+self.data.splitlines()[self.linenum-1]+'\x1b[0m'
            self.show_error(error_class, {'line': self.linenum, 'char': char})

    def show_error(self, error_class, lexer_object):
        text = '[ERROR] "{}", line {}'.format(
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

    def get_tokens(self, t='all'):
        if t == 'onlytoken':
            return [i[0]['tokens'] for i in self.TOKENS if i[0]['tokens'] != []]
        if self.lex_type == 'condition':
            return self.TOKENS
        return [i for i in self.TOKENS if i[0]['tokens'] != []]

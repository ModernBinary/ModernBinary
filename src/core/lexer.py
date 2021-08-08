from os import error
import sys
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

        for char in self.data:
            self.ind += 1

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
                    self.if_statement = False
                    self.if_commands = True
                continue

            if char == '[' or char == ']':
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

            if char == '(' or char == ')':
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
            
            error_class = MBSyntaxError
            error_class.description = 'invalid syntax : \x1b[31m'+self.data.splitlines()[self.linenum-1]+'\x1b[0m'
            self.show_error(error_class, {'line': self.linenum, 'char': char})

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

    def get_tokens(self, t='all'):
        if t == 'onlytoken':
            return [i[0]['tokens'] for i in self.TOKENS if i[0]['tokens'] != []]
        if self.lex_type == 'condition':
            return self.TOKENS
        return [i for i in self.TOKENS if i[0]['tokens'] != []]

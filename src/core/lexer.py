import sys

from core.errors import MBSyntaxError

class Lexer:
    def __init__(self, data) -> None:

        self.data = data+'\n'
        
        self.TOKENS = self.Load_Tokens()
        
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

            self.on_if = ''

            self.if_commands = False

        Reset()

        self.linenum = 1

        for char in self.data:
            self.ind += 1

            if self.if_commands:
                if char != '}':
                    self.on_if += char
                else:
                    complete = [i for i in Lexer(self.on_if.strip()).get_tokens(t='onlytoken')]
                    iftoks = ['IF', self.condition, 'THEN', complete, 'ENDIF']
                    TOKENS.append(iftoks)
                    yield {
                        'line': self.linenum,
                        'endline': self.linenum+self.on_if.strip().count('\n'),
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
            
            yield MBSyntaxError, {'line': self.linenum, 'char': char}

    def get_tokens(self, t='all'):
        if t == 'onlytoken':
            return [i[0]['tokens'] for i in self.TOKENS if i[0]['tokens'] != []]
        return [i for i in self.TOKENS if i[0]['tokens'] != []]
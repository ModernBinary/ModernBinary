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

            self.is_more = False

            self.pr_count = 0

            self.collect_type = ''
            
            self.cr_count = 0

            self.cr_state = False

            self.pr_state = False

            self.line_cache = []

        Reset()

        self.linenum = 1

        for char in self.data:

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

    def get_tokens(self):
        return [i for i in self.TOKENS if i[0]['tokens'] != []]
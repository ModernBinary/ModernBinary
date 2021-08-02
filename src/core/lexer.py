import sys

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

            self.pr_state = False

            self.line_cache = []

        Reset()

        self.linenum = 1

        for char in self.data:
            if char == '(' or char == ')':
                self.pr_state = True if char == '(' else False
                if self.is_more:
                    self.cache = 'VAL:'+self.cache
                if not self.pr_state:
                    if self.is_first:
                        self.is_first = False
                        self.cache = 'ACTION:'+self.cache
                    self.line_cache.append(self.cache)
                    self.pr_count += 1

                self.cache = ''
                continue
            
            if char == ':' or char == '=':
                self.is_more = True
                continue
            
            if char == '\n' or char == self.data[-1]:
                TOKENS.append(self.line_cache)

                yield {
                    'line': self.linenum,
                    'pr_count': self.pr_count,
                    'tokens': self.line_cache
                }

                Reset()
                self.linenum += 1
                continue

            if self.pr_state:
                self.cache += char
                continue


    def get_tokens(self):
        return self.TOKENS
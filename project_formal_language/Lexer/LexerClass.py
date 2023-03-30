import re

class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column
    
    def print_token(self):
        print(f"Token(type={self.kind}, value='{self.value}', line={self.line}, column={self.column})")

class Lexer:
    def __init__(self, code):
        self.code = code
        
    def tokenize(self):
        code = self.code
        keywords = {"SELECT", "FROM", "WHERE", "ORDER_BY"}
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
            ('ALL',      r'\*'),            # All parameter
            ('COMPARATOR', r'(==|>=|<=|<>|>|<)'),        # Comparator operators
            ('COMMA',    r','),            # Comma identifier
            ('END',      r';'),            # Statement terminator
            ('ID',       r'[a-zA-Z][a-zA-Z_$0-9]+'),    # Identifiers
            ('NEWLINE',  r'\n'),           # Line endings
            ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
            ('MISMATCH', r'.'),            # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        line_num = 1
        line_start = 0
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'ID' and value in keywords:
                kind = value
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value} unexpected on line {line_num}')
            result = Token(kind, value, line_num, column)
            result.print_token()
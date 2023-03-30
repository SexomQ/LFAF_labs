# Topic: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Tudor Sclifos

----

## Theory
&ensp;&ensp;&ensp; The term lexer comes from lexical analysis which, in turn, represents the process of extracting lexical tokens from a string of characters. There are several alternative names for the mechanism called lexer, for example tokenizer or scanner. The lexical analysis is one of the first stages used in a compiler/interpreter when dealing with programming, markup or other types of languages.

&ensp;&ensp;&ensp; The tokens are identified based on some rules of the language and the products that the lexer gives are called lexemes. So basically the lexer is a stream of lexemes. Now in case it is not clear what's the difference between lexemes and tokens, there is a big one. The lexeme is just the byproduct of splitting based on delimiters, for example spaces, but the tokens give names or categories to each lexeme. So the tokens don't retain necessarily the actual value of the lexeme, but rather the type of it and maybe some metadata.

## Objectives:
1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Implementation description
* Firstly, I created a class with a method to print the output more readable.
```
class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column
    
    def print_token(self):
        print(f"Token(type={self.kind}, value='{self.value}', line={self.line}, column={self.column}")
```
* Next, I created a class Lexer that encapsulates the method tokenize().
```
class Lexer:
    def __init__(self, code):
        self.code = code
        
    def tokenize(self):
        ...
```
* In tokenize() there is the functionality for lexer. I defined some keywords and token specifications using regex. After that, I went through every character getting the tokens and their positions.
```
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
```
## Conclusions / Screenshots / Results

In conclusion, I managed to convert a finite automaton to grammar, to check if the automaton is deterministic and transform from NDFA to DFA.

<b>Results:</b>
* Lexer test:
```
code_test = '''
    SELECT
        col1,
        col2,
        col3
    FROM table1 WHERE col1 >= 30
    ORDER_BY col2;
    
    SELECT col4 FROM table2 WHERE 1==1;
'''

lexer = Lexer(code_test)
tokens = lexer.tokenize()

------------------------------------------------------------------------------
Token(type=SELECT, value='SELECT', line=2, column=4)
Token(type=ID, value='col1', line=3, column=8)
Token(type=COMMA, value=',', line=3, column=12)
Token(type=ID, value='col2', line=4, column=8)
Token(type=COMMA, value=',', line=4, column=12)
Token(type=ID, value='col3', line=5, column=8)
Token(type=FROM, value='FROM', line=6, column=4)
Token(type=ID, value='table1', line=6, column=9)
Token(type=WHERE, value='WHERE', line=6, column=16)
Token(type=ID, value='col1', line=6, column=22)
Token(type=COMPARATOR, value='>=', line=6, column=27)
Token(type=NUMBER, value='30', line=6, column=30)
Token(type=ORDER_BY, value='ORDER_BY', line=7, column=4)
Token(type=ID, value='col2', line=7, column=13)
Token(type=END, value=';', line=7, column=17)
Token(type=SELECT, value='SELECT', line=9, column=4)
Token(type=ID, value='col4', line=9, column=11)
Token(type=FROM, value='FROM', line=9, column=16)
Token(type=ID, value='table2', line=9, column=21)
Token(type=WHERE, value='WHERE', line=9, column=28)
Token(type=NUMBER, value='1', line=9, column=34)
Token(type=COMPARATOR, value='==', line=9, column=35)
Token(type=NUMBER, value='1', line=9, column=37)
Token(type=END, value=';', line=9, column=38)
```

## References
* https://regex101.com/
* https://docs.python.org/3/library/re.html#writing-a-tokenizer
* https://alpaca.point.space/
* https://chat.openai.com/chat
* https://github.com/DrVasile/FLFA-Labs
* https://github.com/ninico11/FLFA-Labs/tree/main/Reports

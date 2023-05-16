# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Tudor Sclifos

----

## Theory
A parser is a computer program that reads input in a particular format (such as a programming language or a markup language) and generates a structured representation of the input. The structured representation can then be used for further processing, such as interpretation or compilation.

There are several ways to program a parser, depending on the programming language and tools being used. Here are some common steps involved in building a parser:

1. Define the grammar: The first step in building a parser is to define the grammar of the language you want to parse. A grammar is a formal specification of the syntax of the language. There are different types of grammars, such as context-free grammars (CFGs), which are often used for parsing programming languages. You can define the grammar using a grammar notation such as BNF or EBNF.

2. Choose a parsing algorithm: There are several parsing algorithms to choose from, such as recursive descent parsing, LL parsing, LR parsing, or Earley parsing. Each algorithm has its strengths and weaknesses, and the choice of algorithm depends on the complexity of the grammar and the performance requirements of the parser.

3. Implement the parser: Once you have defined the grammar and chosen a parsing algorithm, you can start implementing the parser. This involves writing code that reads input from a source (such as a file or a stream), tokenizes the input into a stream of tokens, and applies the parsing algorithm to generate a parse tree or an abstract syntax tree (AST). The parse tree or AST represents the structured representation of the input.

4. Handle errors: Parsing can fail if the input does not conform to the grammar. In such cases, the parser should report an error and recover gracefully. Error recovery can involve techniques such as backtracking, panic mode recovery, or error productions.

5. Use the output: Once the input has been parsed and a structured representation has been generated, you can use the output for further processing. For example, if you are parsing a programming language, you can use the parse tree or AST for type checking, code generation, or optimization.

Overall, building a parser involves a combination of language theory, algorithms, and programming. It can be a challenging task, but there are many tools and libraries available that can simplify the process.

## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed.
2. Get familiar with the concept of AST.
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation description
First of all I implemented a tree type class (__*ParseTreeNode*__) to define the parsing tree. It has 2 methods: add_child() and print_tree().
The main method, print_tree(), returns a parse tree. It travers all the nodes and its children, colecting them in a string.
```jupyterpython
    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        result = "\t" * level + f"{self.kind}"
        print(result)
        if self.value:
            result += f": {self.value}"
        result += "\n"
        for child in self.children:
            result += child.print_tree(level + 1)
        return result
```
Next, I implemented the parser that has 5 main methods to parse a string: parse(), expect(), advance() and current_token().

The parse() method get the string and determine what it has to parse next.
  ```jupyterpython
   def parse(self):
       if self.current_token() == 'SELECT':
           return self.select_statement()
   ```
The expect() method checks if the current token matches one of the expected kinds and returns a parse tree node representing the token if it does. If the current token does not match any of the expected kinds, it raises a RuntimeError.
  ```jupyterpython
   def expect(self, *expected_kinds):
     if self.current_token().kind not in expected_kinds:
         raise RuntimeError(f'Error: expected {expected_kinds}, but got {self.current_token().kind} at line {self.current_token().line}, column {self.current_token().column}')
     node = ParseTreeNode(self.current_token().kind, self.current_token().value, line=self.current_token().line, column=self.current_token().column)
     self.advance()
     return node
   ```
The advance() method moves on the next token.
  ```jupyterpython
    def advance(self):
     self.current_token_index += 1
   ```
The current_token() and peek() methods help to understand what are the current and next token in the list.
  ```jupyterpython
    def current_token(self):
        return self.tokens[self.current_token_index]
    
    def peek(self):
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        else:
            return Token('', '', 0, 0)
   ```
Then, I wrote the logic for SELECT statement parsing:
    
select_statement(self): This function represents the parsing of a SELECT statement in SQL. It creates a parse tree node with the label 'SELECT_STATEMENT'. It adds child nodes based on the structure of the SELECT statement.
  ```jupyterpython
    def select_statement(self):
        node = ParseTreeNode('SELECT_STATEMENT')
        node.add_child(self.expect('SELECT'))
        if self.current_token().kind == 'ALL':
            node.add_child(self.expect('ALL'))
        else:
            node.add_child(self.list_ids())
        node.add_child(self.expect('FROM'))
        node.add_child(self.expect('ID'))
        if self.current_token().kind == 'WHERE':
            node.add_child(self.where_clause())
        if self.current_token().kind == 'ORDER_BY':
            node.add_child(self.order_by_clause())
        node.add_child(self.expect('END'))
        return node
```
where_clause(self): This function represents the parsing of a WHERE clause in SQL. It checks if there are more tokens available and creates a parse tree node with the label 'WHERE_CLAUSE' if the current token is 'WHERE'. It adds child nodes for the 'WHERE' token and the expression (handled by expression()).
  ```jupyterpython
    def where_clause(self):
        if self.current_token_index + 1 < len(self.tokens):
            node = ParseTreeNode('WHERE_CLAUSE')
            if self.current_token().kind == 'WHERE':
                node.add_child(self.expect('WHERE'))
                node.add_child(self.expression())
            return node
```
order_by_clause(self): This function represents the parsing of an ORDER BY clause in SQL. It checks if there are more tokens available and creates a parse tree node with the label 'ORDER_BY_CLAUSE' if the current token is 'ORDER_BY'. It adds child nodes for the 'ORDER_BY' token and the 'ID' token.
  ```jupyterpython
     def order_by_clause(self):
        if self.current_token_index + 1 < len(self.tokens):
            node = ParseTreeNode('ORDER_BY_CLAUSE')
            if self.current_token().kind == 'ORDER_BY':
                node.add_child(self.expect('ORDER_BY'))
                node.add_child(self.expect('ID'))
            return node
```
expression(self): This function represents the parsing of an expression in SQL. It creates a parse tree node with the label 'EXPRESSION' and adds child nodes for an 'ID' token, a 'COMPARATOR' token, and a 'NUMBER' token.
  ```jupyterpython
    def expression(self):
        node = ParseTreeNode('EXPRESSION')
        node.add_child(self.expect('ID'))
        node.add_child(self.expect('COMPARATOR'))
        node.add_child(self.expect('NUMBER'))
        return node
```
list_ids(self): This function represents the parsing of a list of identifiers in SQL, such as column names.
  ```jupyterpython
    def list_ids(self):
        node = ParseTreeNode('COLUMN_LIST')

        def is_id():
            node.add_child(self.expect('ID'))
            if self.current_token().kind == 'COMMA':
                self.expect('COMMA')
                is_id()
            
        is_id()
        return node
```
## Conclusions / Screenshots / Results

By implementing this parser, it becomes possible to validate and extract information from SQL statements, providing a foundation for further processing or analysis. The parse tree can be utilized to understand the structure of the SQL statement, perform semantic analysis, and potentially generate executable code or perform optimizations. The code snippet focuses on parsing the SELECT statement, WHERE clause, ORDER BY clause, and simple expressions. In a real-world scenario, a SQL parser would need to handle a broader range of SQL syntax, including other types of statements, subqueries, complex expressions, joins, and more.

<b>Results:</b>
* Parser tree:

```jupyterpython
code_test2 = '''SELECT name, age, address FROM customers WHERE age > 25 ORDER_BY name;'''

lexer = Lexer(code_test2)
tokens = lexer.tokenize()
parser = Parser(tokens)
parse_tree = parser.parse()
print(parse_tree.print_tree())
```
Result:
```
SELECT_STATEMENT
	SELECT: SELECT
	COLUMN_LIST
		ID: name
		ID: age
		ID: address
	FROM: FROM
	ID: customers
	WHERE_CLAUSE
		WHERE: WHERE
		EXPRESSION
			ID: age
			COMPARATOR: >
			NUMBER: 25
	ORDER_BY_CLAUSE
		ORDER_BY: ORDER_BY
		ID: name
	END: ;
```

## References
* [Parsing Wiki](https://en.wikipedia.org/wiki/Parsing)
* [Abstract Syntax Tree Wiki](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
* [Chat GPT](https://chat.openai.com/?model=text-davinci-002-render-sha)
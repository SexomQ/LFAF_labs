from Parser.ParseTreeNodeClass import ParseTreeNode
from project_formal_language.Lexer.TokenClass import Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        
    def parse(self):
        if self.current_token() == 'SELECT':
            return self.select_statement()
    
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
    
    def where_clause(self):
        if self.current_token_index + 1 < len(self.tokens):
            node = ParseTreeNode('WHERE_CLAUSE')
            if self.current_token().kind == 'WHERE':
                node.add_child(self.expect('WHERE'))
                node.add_child(self.expression())
            return node
            
    def order_by_clause(self):
        if self.current_token_index + 1 < len(self.tokens):
            node = ParseTreeNode('ORDER_BY_CLAUSE')
            if self.current_token().kind == 'ORDER_BY':
                node.add_child(self.expect('ORDER_BY'))
                node.add_child(self.expect('ID'))
            return node
            
    def expression(self):
        node = ParseTreeNode('EXPRESSION')
        node.add_child(self.expect('ID'))
        node.add_child(self.expect('COMPARATOR'))
        node.add_child(self.expect('NUMBER'))
        return node
    
    def list_ids(self):
        node = ParseTreeNode('COLUMN_LIST')

        def is_id():
            node.add_child(self.expect('ID'))
            if self.current_token().kind == 'COMMA':
                self.expect('COMMA')
                is_id()
            
        is_id()
        return node
        
    def expect(self, *expected_kinds):
        if self.current_token().kind not in expected_kinds:
            raise RuntimeError(f'Error: expected {expected_kinds}, but got {self.current_token().kind} at line {self.current_token().line}, column {self.current_token().column}')
        node = ParseTreeNode(self.current_token().kind, self.current_token().value, line=self.current_token().line, column=self.current_token().column)
        self.advance()
        return node
        
    def current_token(self):
        return self.tokens[self.current_token_index]
    
    def peek(self):
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        else:
            return Token('', '', 0, 0)
        
    def advance(self):
        self.current_token_index += 1

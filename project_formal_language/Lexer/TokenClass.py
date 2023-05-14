class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column
    
    def print_token(self):
        return f"Token(type={self.kind}, value='{self.value}', line={self.line}, column={self.column})"
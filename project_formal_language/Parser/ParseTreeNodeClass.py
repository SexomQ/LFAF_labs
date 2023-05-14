class ParseTreeNode:
    def __init__(self, kind, value=None, children=None, line=0, column=0):
        self.kind = kind
        self.value = value
        self.children = children or []
        self.line = line
        self.column = column

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        result = "\t" * level + f"{self.kind}"
        if self.value:
            result += f": {self.value}"
        result += "\n"
        for child in self.children:
            result += child.print_tree(level + 1)
        return result
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'
    
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.tok}, {self.right_node})'
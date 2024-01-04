class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'
    
class DecimalNode(NumberNode):
    def __init__(self, tok):
        super().__init__(tok)
    
class BoolNode(NumberNode):
    def __init__(self, tok):
        super().__init__(tok)

class IdAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end
    
class IntAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end
class FloatAssignNode(IntAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)
        
class BoolAssignNode(IntAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)
    
class ArithOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'({self.op_tok.type}, {self.node})'
    
class AskNode:
    def __init__(self, cases, more_case):
        self.cases = cases
        self.more_case = more_case

        self.pos_start = self.cases[0][0].pos_start

        if self.more_case:
            self.pos_end = self.more_case[-1:][0].pos_end
        else:
            self.pos_end = self.cases[-1:][0].pos_end
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

class StringNode(NumberNode):
    def __init__(self, tok):
        super().__init__(tok)

class CharNode(NumberNode):
    def __init__(self, tok):
        super().__init__(tok)

class IdAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class IdAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end
    
class IntAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

class FloatAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)
        
class BoolAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

class CharAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

class StringAssignNode(IdAssignNode):
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
    
class IncrementNode:
    def __init__(self, var_name_tok, op_tok1, op_tok2):
        self.var_name_tok = var_name_tok
        self.op_tok1 = op_tok1
        self.op_tok2 = op_tok2

        self.pos_start = var_name_tok.pos_start
        self.pos_end = op_tok2.pos_end
    
class AskNode:
    def __init__(self, cases, more_case):
        self.cases = cases
        self.more_case = more_case

        self.pos_start = self.cases[0][0].pos_start

        if self.more_case:
            self.pos_end = self.more_case.pos_end
        else:
            self.pos_end = self.cases[len(self.cases) - 1][0].pos_end

class RepeatNode:
    def __init__(self, var_name_tok, value_node, cond_node, iter_node, body_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.cond_node = cond_node
        self.iter_node = iter_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

class WhileNode:
    def __init__(self, cond_node, body_node):
        self.cond_node = cond_node
        self.body_node = body_node

        self.pos_start = self.cond_node.pos_start
        self.pos_end = self.body_node.pos_end

class BuildDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end
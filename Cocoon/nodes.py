class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self, indent=0):
        return f'{self.tok.__repr__(indent)}'
    
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

class UndefinedNode():
    def __init__(self):
        self.tok = None
        
        self.pos_start = None
        self.pos_end = None

    def __repr__(self, indent=0):
        return f'{self.tok}'

class IdDeclareNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self, indent=0):
        node_str = f'type: "IdDeclareNode",\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class numDeclareNode(IdDeclareNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "numDeclareNode",\n{" " * (indent + 4)}accepted data type: Number,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'


class deciDeclareNode(IdDeclareNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "deciDeclareNode",\n{" " * (indent + 4)}accepted data type: Decimal,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class boolDeclareNode(IdDeclareNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "boolDeclareNode",\n{" " * (indent + 4)}accepted data type: Bool,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class charDeclareNode(IdDeclareNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "charDeclareNode",\n{" " * (indent + 4)}accepted data type: Character,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class textDeclareNode(IdDeclareNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "textDeclareNode",\n{" " * (indent + 4)}accepted data type: Text,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class IdAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end
        
    def __repr__(self, indent=0):
        node_str = f'type: "IdAccessNode",\n'
        var_str = f'{" " * (indent + 4)}target variable: {self.var_name_tok.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}\n{" " * indent}}}'

class IdAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self, indent=0):
        node_str = f'type: "IdAssignNode",\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'
    
class numAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "numAssignNode",\n{" " * (indent + 4)}accepted data type: Number,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'
class deciAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)
        
    def __repr__(self, indent=0):
        node_str = f'type: "deciAssignNode",\n{" " * (indent + 4)}accepted data type: Decimal,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class boolAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "boolAssignNode",\n{" " * (indent + 4)}accepted data type: Bool,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class charAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "charAssignNode",\n{" " * (indent + 4)}accepted data type: Character,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'

class textAssignNode(IdAssignNode):
    def __init__(self, var_name_tok, value_node):
        super().__init__(var_name_tok, value_node)

    def __repr__(self, indent=0):
        node_str = f'type: "textAssignNode",\n{" " * (indent + 4)}accepted data type: Text,\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}value: {self.value_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}\n{" " * indent}}}'
    
class ArithOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self, indent=0):
        op_str = f'type: "ArithOpNode",\n{" " * (indent + 4)}operator: {self.op_tok.__repr__(indent + 4)},\n'
        left_str = f'{" " * (indent + 4)}left node: {self.left_node.__repr__(indent + 4)},\n'
        right_str = f'{" " * (indent + 4)}right node: {self.right_node.__repr__(indent + 4)}'
        return f'{{\n{" " * indent}{op_str}{left_str}{right_str}\n{" " * indent}}}'
    
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self, indent=0):
        op_str = f'type: "UnaryOpNode",\n{" " * (indent + 4)}operator: {self.op_tok.__repr__(indent + 4)},\n'
        right_str = f'{" " * (indent + 4)}right node: {self.node.__repr__(indent + 4)}'
        return f'{{\n{" " * (indent)}{op_str}{right_str}\n{" " * indent}}}'
    
class IncrementNode:
    def __init__(self, var_name_tok, op_tok1, op_tok2):
        self.var_name_tok = var_name_tok
        self.op_tok1 = op_tok1
        self.op_tok2 = op_tok2

        self.pos_start = var_name_tok.pos_start
        self.pos_end = op_tok2.pos_end

    def __repr__(self, indent=0):
        op_str = f'type: "IncrementNode",\n{" " * (indent + 4)}operators: {self.op_tok1.__repr__(indent + 4)}, {self.op_tok2.__repr__(indent + 4)},\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)}'
        return f'{{\n{" " * (indent)}{op_str}{var_str}\n{" " * indent}}}'
    
class AskNode:
    def __init__(self, cases, more_case):
        self.cases = cases
        self.more_case = more_case

        self.pos_start = self.cases[0][0].pos_start

        if self.more_case:
            self.pos_end = self.more_case[0].pos_end
        else:
            self.pos_end = (self.cases[len(self.cases) - 1])[0].pos_end

#!! hinde mo pa naaayos repr nito
            
    def __repr__(self, indent=0):
        node_str = f'type: "AskNode",\n'
        if_elif_cases_str = f'{" " * (indent + 4)}if and elif cases: {self.cases},\n'
        if self.more_case:
            else_case_str = f'{" " * (indent + 4)}else case: None'
        else:
            else_case_str = f'{" " * (indent + 4)}else case: {self.more_case}'
        return f'{{\n{" " * indent}{node_str}{if_elif_cases_str}{else_case_str}\n{" " * indent}}}'

class RepeatNode:
    def __init__(self, var_name_tok, value_node, cond_node, iter_node, body_node, should_return_empty):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.cond_node = cond_node
        self.iter_node = iter_node
        self.body_node = body_node
        self.should_return_empty = should_return_empty

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self, indent=0):
        node_str = f'type: "RepeatNode",\n'
        var_str = f'{" " * (indent + 4)}variable name: {self.var_name_tok.__repr__(indent + 4)},\n'
        value_str = f'{" " * (indent + 4)}initial value: {self.value_node.__repr__(indent + 4)},\n'
        cond_str = f'{" " * (indent + 4)}repeat condition: {self.cond_node.__repr__(indent + 4)},\n'
        iter_str = f'{" " * (indent + 4)}iteration node: {self.iter_node.__repr__(indent + 4)},\n'
        body_str = f'{" " * (indent + 4)}body node: {self.body_node.__repr__(indent + 4)},\n'
        return_str = f'{" " * (indent + 4)}should return empty: {self.should_return_empty}'
        return f'{{\n{" " * indent}{node_str}{var_str}{value_str}{cond_str}{iter_str}{body_str}{return_str}\n{" " * indent}}}'

class WhileNode:
    def __init__(self, cond_node, body_node, should_return_empty):
        self.cond_node = cond_node
        self.body_node = body_node
        self.should_return_empty = should_return_empty

        self.pos_start = self.cond_node.pos_start
        self.pos_end = self.body_node.pos_end

    def __repr__(self, indent=0):
        node_str = f'type: "WhileNode",\n'
        cond_str = f'{" " * (indent + 4)}while condition: {self.cond_node.__repr__(indent + 4)},\n'
        body_str = f'{" " * (indent + 4)}body node: {self.body_node.__repr__(indent + 4)},\n'
        return_str = f'{" " * (indent + 4)}should return empty: {self.should_return_empty}'
        return f'{{\n{" " * indent}{node_str}{cond_str}{body_str}{return_str}\n{" " * indent}}}'

class BuildDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_return_empty):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_return_empty = should_return_empty

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end
    
    def __repr__(self, indent=0):
        node_str = f'type: "BuildDefNode",\n'
        if self.var_name_tok and len(self.arg_name_toks) == 0:
            var_str = f'{" " * (indent + 4)}build: {self.var_name_tok.__repr__(indent + 4)},\n'
            body_str = f'{" " * (indent + 4)}body node: {self.body_node.__repr__(indent + 4)},\n'
            empty_str = f'{" " * (indent + 4)}should return empty: {self.should_return_empty}'
            return f'{{\n{" " * indent}{node_str}{var_str}{body_str}{empty_str}\n{" " * indent}}}'
        elif self.var_name_tok and len(self.arg_name_toks) > 0:
            var_str = f'{" " * (indent + 4)}build: {self.var_name_tok.__repr__(indent + 4)},\n'
            arg_name_str= ''
            if len(self.arg_name_toks) == 1:
                arg_name_str += f'{" " * (indent + 4)}argument1: {self.arg_name_toks[0].__repr__(indent + 4)},\n'
            else:
                for idx, arg in enumerate(self.arg_name_toks, start=1):
                    arg_name_str += f'{" " * (indent + 4)}argument{idx}: {arg.__repr__(indent + 4)},\n'
            body_str = f'{" " * (indent + 4)}body node: {self.body_node.__repr__(indent + 4)},\n'
            empty_str = f'{" " * (indent + 4)}should return empty: {self.should_return_empty}'
            return f'{{\n{" " * indent}{node_str}{var_str}{arg_name_str}{body_str}{empty_str}\n{" " * indent}}}'
        else:
            var_str = f'{" " * (indent + 4)}build: <anonymous>,\n'
            arg_name_str = ''
            if len(self.arg_name_toks) == 1:
                arg_name_str += f'{" " * (indent + 4)}argument1: {self.arg_name_toks[0].__repr__(indent + 4)},\n'
            else:
                for idx, arg in enumerate(self.arg_name_toks, start=1):
                    arg_name_str += f'{" " * (indent + 4)}argument{idx}: {arg.__repr__(indent + 4)},\n'
            body_str = f'{" " * (indent + 4)}body node: {self.body_node.__repr__(indent + 4)},\n'
            empty_str = f'{" " * (indent + 4)}should return empty: {self.should_return_empty}'
            return f'{{\n{" " * indent}{node_str}{var_str}{arg_name_str}{body_str}{empty_str}\n{" " * indent}}}'

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

    def __repr__(self, indent=0):
        node_str = f'type: "CallNode",\n'
        node_to_call_str = f'{" " * (indent + 4)}node to call: {self.node_to_call.__repr__(indent + 4)},\n'
        if len(self.arg_nodes) == 1:
            arg_nodes_str = f'{" " * (indent + 4)}arguments: {self.arg_nodes[0].__repr__(indent + 4)}\n'
        else:
            arg_nodes_str = ''
            for idx, arg in enumerate(self.arg_nodes, start=1):
                arg_nodes_str += f'{" " * (indent + 4)}argument{idx}: {arg.__repr__(indent + 4)},\n'

        return f'{{\n{" " * indent}{node_str}{node_to_call_str}{arg_nodes_str}{" " * indent}}}'

class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self, indent=0):
        node_str = f'type: "ListNode",\n'
        if len(self.element_nodes) == 1:
            elements_str = f'{" " * (indent + 4)}element: {self.element_nodes[0].__repr__(indent + 4)}\n'
        else:
            elements_str = ''
            for idx, element in enumerate(self.element_nodes, start=1):
                if idx == len(self.element_nodes):
                    elements_str += f'{" " * (indent + 4)}element{idx}: {element.__repr__(indent + 4)}\n'
                else:
                    elements_str += f'{" " * (indent + 4)}element{idx}: {element.__repr__(indent + 4)},\n'

        return f'{{\n{" " * indent}{node_str}{elements_str}{" " * indent}}}'
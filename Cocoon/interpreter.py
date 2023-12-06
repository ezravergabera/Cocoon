from .values import Number
from .tokentypes import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_INTDIV, TT_EXPO, TT_MOD, TT_POSITIVE, TT_NEGATIVE
from icecream import ic

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node):
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    def visit_ArithOpNode(self, node):
        left = ic(self.visit(node.left_node))
        right = self.visit(node.right_node)

        if ic(node.op_tok.type == TT_PLUS):
            result = ic(left.added_to(right))
        elif node.op_tok.type == TT_MINUS:
            result = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result = left.multiplied_by(right)
        elif node.op_tok.type == TT_DIV:
            result = left.divided_by(right)
        elif node.op_tok.type == TT_INTDIV:
            result = left.intdivided_by(right)
        elif node.op_tok.type == TT_EXPO:
            result = left.raised_to(right)
        elif node.op_tok.type == TT_MOD:
            result = left.mod(right)

        return result.set_pos(node.pos_start, node.pos_end)

    def visit_UnaryOpNode(self, node):
        number = self.visit(node.node)

        if node.op_tok.value == TT_POSITIVE:
            number = number.multiplied_by(Number(1))
        elif node.op_tok.value == TT_NEGATIVE:
            number = number.multiplied_by(Number(-1))

        return number.set_pos(node.pos_start, node.pos_end)
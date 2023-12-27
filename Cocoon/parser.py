from .nodes import NumberNode, ArithOpNode, UnaryOpNode
from .tokentypes import TT_INT, TT_FLOAT, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_INTDIV, TT_EXPO, TT_MOD, TT_POSITIVE, TT_NEGATIVE, TT_LPAREN, TT_RPAREN, TT_EOF
from .errors import InvalidSyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_tok = self.tokens[self.token_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Error")) # TODO: figure out what error message should be here
        return res

    # Production Rules
    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected a closing symbol ')'"))
            
        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        
        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, '+', '-' or '('"))
            
    def power(self):
        return self.arith_op(self.atom, (TT_EXPO, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_POSITIVE, TT_NEGATIVE):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        return self.power()

    def term(self):
        return self.arith_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.arith_op(self.term, (TT_PLUS, TT_MINUS, TT_INTDIV, TT_MOD))

    def arith_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func_b())
            if res.error: return res
            left = ArithOpNode(left, op_tok, right)

        return res.success(left)
    
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: 
                self.error = res.error
            return res.node
        
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

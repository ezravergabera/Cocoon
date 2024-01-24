from .nodes import NumberNode, DecimalNode, BoolNode, StringNode, CharNode, ListNode, UndefinedNode, numDeclareNode, deciDeclareNode, boolDeclareNode, charDeclareNode, textDeclareNode, IdAccessNode, IdAssignNode, IntAssignNode, FloatAssignNode, BoolAssignNode, CharAssignNode, StringAssignNode, ArithOpNode, UnaryOpNode, IncrementNode, AskNode, RepeatNode, WhileNode, BuildDefNode, CallNode
from .tokentypes import TT_ID, TT_ASSIGN, TT_INT, TT_FLOAT, TT_STR, TT_BOOL, TT_CHAR, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_INTDIV, TT_EXPO, TT_MOD, TT_GREATER, TT_LESS, TT_GREATEREQUAL, TT_LESSEQUAL, TT_EQUALTO, TT_NOTEQUAL, TT_NOT, TT_AND, TT_OR, TT_DTYPE, TT_KWORD, TT_RWORD, TT_NWORD, TT_COMMENT, TT_COMMA, TT_SEMICOLON, TT_LSQUARE, TT_RSQUARE, TT_LPAREN, TT_RPAREN, TT_NEWLINE, TT_EOF
from .errors import InvalidSyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        self.update_current_tok()
        return self.current_tok
    
    def backtrack(self):
        self.token_idx -= 1
        self.update_current_tok()
        return self.current_tok
    
    def reverse(self, amount=1):
        self.token_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.token_idx < len(self.tokens):
            self.current_tok = self.tokens[self.token_idx]

    def parse(self):
        res = self.root()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Parse Error"))
        return res

    # Production Rules
    def build_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_RWORD, "build"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'build'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_ID:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_ID:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_ID:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected an identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')' or ','"
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected an identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_LSQUARE:
            res.register_advancement()
            self.advance()

            node_to_return = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            else:
                res.register_advancement()
                self.advance()

            if res.error: return res
            return res.success(BuildDefNode(var_name_tok, arg_name_toks, node_to_return, False))
        
        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            note_to_return = res.register(self.statements())
            if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            
            res.register_advancement()
            self.advance()

            return res.success(BuildDefNode(var_name_tok, arg_name_toks, note_to_return, True))

    def assign_expr(self):
        res = ParseResult()

        if self.current_tok.type == TT_ID:
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.matches(TT_RWORD, 'ask'):
                ask_expr = res.register(self.ask_expr())
                if res.error: return res
                return res.success(IdAssignNode(var_name, ask_expr))

            expr = res.register(self.expr())
            if res.error: return res
            return res.success(IdAssignNode(var_name, expr))

    def incre_expr(self):
        res = ParseResult()

        if self.current_tok.type == TT_ID:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_PLUS:
                op_tok1 = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == TT_PLUS:
                    op_tok2 = self.current_tok
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected '+'"
                    ))

            if self.current_tok.type == TT_MINUS:
                op_tok1 = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == TT_MINUS:
                    op_tok2 = self.current_tok
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected '-'"
                    ))

            if res.error: return res
            return res.success(IncrementNode(var_name_tok, op_tok1, op_tok2))
        
    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_RWORD, "while"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'while'"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"
            ))
        else:
            res.register_advancement()
            self.advance()

        cond_node = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')'"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.matches(TT_NWORD, "do"):
            res.register_advancement()
            self.advance()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.type == TT_NEWLINE:
            body_node = res.register(self.statements())
            if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            
            res.register_advancement()
            self.advance()

            return res.success(WhileNode(cond_node, body_node, True))

        body_node = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TT_SEMICOLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ';'"
            ))
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            body_node = res.register(self.statements())
            if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            res.register_advancement()
            self.advance()

            return res.success(WhileNode(cond_node, body_node, True))

        if res.error: return res
        return res.success(WhileNode(cond_node, body_node, False))

    def repeat_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_RWORD, "repeat"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'repeat'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.matches(TT_DTYPE, 'num') or self.current_tok.matches(TT_DTYPE, 'number'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ID:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected an identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()

            value_node = res.register(self.expr())
            if res.error: return res

        if self.current_tok.type != TT_SEMICOLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ';'"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.matches(TT_ID, var_name.value):
            cond_node = res.register(self.expr())
            if res.error: return res
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'{var_name.value}' must be used for the condition"
            ))

        if self.current_tok.type != TT_SEMICOLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ';'"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.matches(TT_ID, var_name.value):
            iter_node = res.register(self.expr())
            if res.error: return res
        else:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'{var_name.value}' must be used for the iteration"
            ))

        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')'"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body_node = res.register(self.statements())
            if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            res.register_advancement()
            self.advance()

            return res.success(RepeatNode(var_name, value_node, cond_node, iter_node, body_node, True))
        
        body_node = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TT_SEMICOLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ';'"
            ))
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            body_node = res.register(self.statements())
            if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            res.register_advancement()
            self.advance()

            return res.success(RepeatNode(var_name, value_node, cond_node, iter_node, body_node, True))

        if res.error: return res
        return res.success(RepeatNode(var_name, value_node, cond_node, iter_node, body_node, False))
    
    def ask_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        more_case = None

        if not self.current_tok.matches(TT_RWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))

        res.register_advancement()
        self.advance()
        
        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"
            ))
        else:
            res.register_advancement()
            self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')'"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.matches(TT_NWORD, 'do'):
            res.register_advancement()
            self.advance()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'do' or '['"
            ))
        else:
            res.register_advancement()
            self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            else:
                res.register_advancement()
                self.advance()
            
            if self.current_tok.type == TT_SEMICOLON:
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.askmore_or_more_expr())
                if res.error: return res
                new_cases, more_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr, False))

            if self.current_tok.type != TT_SEMICOLON:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, 
                    "Expected ';'"
                ))
            else:
                res.register_advancement()
                self.advance()

            if self.current_tok.type == TT_RSQUARE:
                res.register_advancement()
                self.advance()
            else:
                statements = res.register(self.statements())
                if res.error: return res
                cases.append((condition, statements, True))

                if self.current_tok.type != TT_RSQUARE:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ']'"
                    ))
                else:
                    res.register_advancement()
                    self.advance()

            if self.current_tok.type == TT_SEMICOLON:
                pass
            else:
                all_cases = res.register(self.askmore_or_more_expr())
                if res.error: return res
                new_cases, more_case = all_cases
                cases.extend(new_cases)

        if res.error: return res
        return res.success((cases, more_case))
    
    def askmore_or_more_expr(self):
        res = ParseResult()
        cases, more_case = [], None

        if self.current_tok.matches(TT_RWORD, 'askmore'):
            all_cases = res.register(self.askmore_expr())
            if res.error: return res
            cases, more_case = all_cases
        else:
            more_case = res.register(self.more_expr())
            if res.error: return res

        return res.success((cases, more_case))

    def ask_expr(self):
        res = ParseResult()
        all_cases = res.register(self.ask_expr_cases('ask'))
        if res.error: return res
        cases, more_case = all_cases
        return res.success(AskNode(cases, more_case))
    
    def askmore_expr(self):
        return self.ask_expr_cases('askmore')
    
    def more_expr(self):
        res = ParseResult()
        more_case = None

        if self.current_tok.matches(TT_RWORD, 'more'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_LSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '['"
                ))
            else:
                res.register_advancement()
                self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res

                if self.current_tok.type != TT_RSQUARE:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ']'"
                    ))
                else:
                    res.register_advancement()
                    self.advance()

                more_case = (statements, True)
            else:
                expr = res.register(self.expr())
                if res.error: return res

                if self.current_tok.type != TT_SEMICOLON:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ';'"
                    ))
                else:
                    res.register_advancement()
                    self.advance()

                if self.current_tok.type == TT_RSQUARE:
                    res.register_advancement()
                    self.advance()
                else:
                    statements = res.register(self.statements())
                    if res.error: return res

                    if self.current_tok != TT_RSQUARE:
                        return res.failure(InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected ']'"
                        ))
                    else:
                        res.register_advancement()
                        self.advance()

                    more_case = (statements, True)
                    if res.error: return res
                    return res.success(more_case)

                more_case = (expr, False)
        if res.error: return res
        return res.success(more_case)
    
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', data type keyword, int, float, identifier, 'true', 'false', 'ask', '+', '-', '(', 'not', or 'NOT'"
                ))
            
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))

            res.register_advancement()
            self.advance()

        if res.error: return res
        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy()))

    def atom(self):
        res = ParseResult()
        tok = self.current_tok
            
        if tok.matches(TT_RWORD, "build"):
            build_def = res.register(self.build_def())
            if res.error: return res
            return res.success(build_def)

        elif tok.matches(TT_RWORD, "while"):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_RWORD, "repeat"):
            repeat_expr = res.register(self.repeat_expr())
            if res.error: return res
            return res.success(repeat_expr)

        elif tok.matches(TT_RWORD, "ask"):
            ask_expr = res.register(self.ask_expr())
            if res.error: return res
            return res.success(ask_expr)
        
        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected a closing symbol ')'"))
            
        elif tok.type == TT_INT:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_FLOAT:
            res.register_advancement()
            self.advance()
            return res.success(DecimalNode(tok))

        elif tok.type == TT_ID or tok.matches(TT_RWORD, "empty") or tok.matches(TT_KWORD, "show") or tok.matches(TT_KWORD, "get"):
            res.register_advancement()
            self.advance()
            pass_ = False

            if self.current_tok.type in (TT_PLUS, TT_MINUS):
                res.register_advancement()
                self.advance()
                if not self.current_tok.type in (TT_PLUS, TT_MINUS):
                    res.register_backtrack()
                    self.backtrack()
                    pass_ = True
                else:
                    res.register_backtrack()
                    self.backtrack()
                    res.register_backtrack()
                    self.backtrack()
                if not pass_:
                    return self.incre_expr()
            
            if self.current_tok.type == TT_ASSIGN:
                res.register_backtrack()
                self.backtrack()
                return self.assign_expr()

            return res.success(IdAccessNode(tok))
        
        elif tok.matches(TT_BOOL, 'true'):
            tok.value = 1
            res.register_advancement
            self.advance()
            return res.success(BoolNode(tok))
        
        elif tok.matches(TT_BOOL, 'false'):
            tok.value = 0
            res.register_advancement
            self.advance()
            return res.success(BoolNode(tok))
        
        elif tok.type == TT_STR:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))
        
        elif tok.type == TT_CHAR:
            res.register_advancement()
            self.advance()
            return res.success(CharNode(tok))
        
        return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, identifier, str, char, 'build', 'while', 'repeat', 'ask', 'true', 'false', 'ask', '+', '-', '(', or ,'['"))
            
    def call(self):
        res = ParseResult()

        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', data type keyword, int, float, identifier, str, char, 'true', 'false', 'ask', '+', '-', '(', 'not', or 'NOT'"
                    ))
                
                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')'"
                    ))

                res.register_advancement()
                self.advance()
                
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def power(self):
        return self.arith_op(self.call, (TT_EXPO, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        return self.power()

    def term(self):
        return self.arith_op(self.factor, (TT_MUL, TT_DIV, TT_INTDIV, TT_MOD))

    def arith_expr(self):
        return self.arith_op(self.term, (TT_PLUS, TT_MINUS))

    def rel_expr(self):
        res = ParseResult()

        if self.current_tok.type == TT_NOT:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.rel_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        
        node = res.register(self.arith_op(self.arith_expr, (TT_GREATER, TT_LESS, TT_GREATEREQUAL, TT_LESSEQUAL, TT_EQUALTO, TT_NOTEQUAL)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                               self.current_tok.pos_start, self.current_tok.pos_end,
                               "Expected int, float, identifier, '+', '-', '(', '[', 'not', or 'NOT'"))
        
        return res.success(node)
    
    def text_assign(self):
        res = ParseResult()

        # text identifier = str
        if self.current_tok.matches(TT_DTYPE, 'text'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ID:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected an identifier'
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_STR and not self.current_tok.matches(TT_KWORD, 'get'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected string literal, or 'get'"
                ))

            string_value = res.register(self.expr())
            if res.error: return res
            return res.success(StringAssignNode(var_name, string_value))
        
        return None
    
    def char_assign(self):
        res = ParseResult()

        # character identifier = char
        if self.current_tok.matches(TT_DTYPE, 'char') or self.current_tok.matches(TT_DTYPE, 'character'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ID:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    'Expected an identifier'
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_CHAR and not self.current_tok.matches(TT_KWORD, 'get'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected char literal, or 'get'"
                ))
            
            char_value = res.register(self.expr())
            if res.error: return res
            return res.success(CharAssignNode(var_name, char_value))
        
        return None
    
    def bool_assign(self):
        res = ParseResult()

        # boolean identifier = bool
        if self.current_tok.matches(TT_DTYPE, 'bool') or self.current_tok.matches(TT_DTYPE, 'boolean'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ID:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected an identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_BOOL and not self.current_tok.matches(TT_KWORD, 'get'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'true', 'false', or 'get'"
                ))

            expr = res.register(self.expr())
            if res.error: return res
            return res.success(BoolAssignNode(var_name, expr))
        
        return None
    
    def  deci_assign(self):
        res = ParseResult()

        # decimal identifier = 1.9
        if self.current_tok.matches(TT_DTYPE, 'deci') or self.current_tok.matches(TT_DTYPE, 'decimal'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ID:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected an identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))
   
            res.register_advancement()
            self.advance()

            # parsing int to float
            if self.current_tok.type == TT_INT:
                self.current_tok.type = TT_FLOAT
                self.current_tok.value = float(self.current_tok.value)

            if self.current_tok.type != TT_FLOAT and not self.current_tok.matches(TT_KWORD, 'get'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected int, float, or 'get'"
                ))
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(FloatAssignNode(var_name, expr))
        
        return None

    def num_assign(self):
        res = ParseResult()

        # num identifier = expr
        if self.current_tok.matches(TT_DTYPE, 'num') or self.current_tok.matches(TT_DTYPE, 'number'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ID:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected an identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()

            #? Kung i automatic parse ba kapag float tok nakuha or hindi nalang tatanggapin as in?

            if self.current_tok.type != TT_INT and not self.current_tok.matches(TT_KWORD, 'get'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected int or 'get'"
                ))
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(IntAssignNode(var_name, expr))
        
        return None
        
    def var_assigns(self):
        if self.current_tok.matches(TT_DTYPE, 'num') or self.current_tok.matches(TT_DTYPE, 'number'):
            return self.num_assign()
        
        elif self.current_tok.matches(TT_DTYPE, 'deci') or self.current_tok.matches(TT_DTYPE, 'decimal'):
            return self.deci_assign()
        
        elif self.current_tok.matches(TT_DTYPE, 'bool') or self.current_tok.matches(TT_DTYPE, 'boolean'):
            return self.bool_assign()
        
        elif self.current_tok.matches(TT_DTYPE, 'char') or self.current_tok.matches(TT_DTYPE, 'character'):
            return self.char_assign()
        
        else:
            return self.text_assign()

    def text_declare(self):
        res = ParseResult()

        node = res.register(self.base_declare())
        if res.error: return res
        return res.success(node)

    def char_declare(self):
        res = ParseResult()

        node = res.register(self.base_declare())
        if res.error: return res
        return res.success(node)

    def bool_declare(self):
        res = ParseResult()

        node = res.register(self.base_declare())
        if res.error: return res
        return res.success(node)

    def deci_declare(self):
        res = ParseResult()

        node = res.register(self.base_declare())
        if res.error: return res
        return res.success(node)

    def num_declare(self):
        res = ParseResult()

        node = res.register(self.base_declare())
        if res.error: return res
        return res.success(node)
    
    def base_declare(self):
        res = ParseResult()

        node = self.current_tok.value

        if node == "num" or node == "number":
            func_name = "num"
        elif node == "deci" or node == "decimal":
            func_name = "deci"
        elif node == "bool" or node == "boolean":
            func_name = "bool"
        elif node == "char" or node == "character":
            func_name = "char"
        elif node == "text":
            func_name = node

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_ID:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected an identifier"
            ))
        else:
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

        if self.current_tok.type == TT_SEMICOLON:
            value = UndefinedNode()
            node_name = f'{func_name}DeclareNode'
            node_class = globals().get(node_name)
            return res.success(node_class(var_name, value))
        else:
            res.register_backtrack()
            self.backtrack()
            res.register_backtrack()
            self.backtrack()

        return res.success(None)
    
    def var_declares(self):
        res = ParseResult()

        if self.current_tok.matches(TT_DTYPE, 'num') or self.current_tok.matches(TT_DTYPE, 'number'):
            node = res.register(self.num_declare())
            if self.current_tok.type == TT_SEMICOLON:
                return res.success(node)
        
        elif self.current_tok.matches(TT_DTYPE, 'deci') or self.current_tok.matches(TT_DTYPE, 'decimal'):
            node = res.register(self.deci_declare())
            if self.current_tok.type == TT_SEMICOLON:
                return res.success(node)
        
        elif self.current_tok.matches(TT_DTYPE, 'bool') or self.current_tok.matches(TT_DTYPE, 'boolean'):
            node = res.register(self.bool_declare())
            if self.current_tok.type == TT_SEMICOLON:
                return res.success(node)
        
        elif self.current_tok.matches(TT_DTYPE, 'char') or self.current_tok.matches(TT_DTYPE, 'character'):
            node = res.register(self.char_declare())
            if self.current_tok.type == TT_SEMICOLON:
                return res.success(node)
        
        elif self.current_tok.matches(TT_DTYPE, 'text'):
            node = res.register(self.text_declare())
            if self.current_tok.type == TT_SEMICOLON:
                return res.success(node)
        
        if res.error: return res
        return self.var_assigns()

    def expr(self):
        res = ParseResult()

        while self.current_tok.type == TT_COMMENT:
            res.register_advancement()
            self.advance()

        if self.current_tok.type == TT_DTYPE:
            node = res.register(self.var_declares())
            if res.error: return res
            return res.success(node)

        node = res.register(self.arith_op(self.rel_expr, (TT_AND, TT_OR)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                               self.current_tok.pos_start, self.current_tok.pos_end,
                               "Expected a data type keyword, int, float, identifier, str, char, 'build', 'while', 'repeat', 'ask', 'true', 'false', '+', '-', '(', '[', 'not', or 'NOT'"))
        
        while self.current_tok.type == TT_COMMENT:
            res.register_advancement()
            self.advance()

        return res.success(node)
    
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.expr())
        if res.error: return res
        statements.append(statement)

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        if self.current_tok.type != TT_SEMICOLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ';'"
            ))
        else:
            res.register_advancement()
            self.advance()

        more_statements = True

        while True:
            res.advance_count = 0
            newline_count = 1
            while self.current_tok.type == TT_NEWLINE and self.current_tok.type != TT_EOF:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements: break
            statement = res.try_register(self.expr())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1

            if self.current_tok.type != TT_SEMICOLON:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ';'"
                ))
            else:
                res.register_advancement()
                self.advance()
                newline_count += 1

        if res.error: return res
        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def root(self):
        res = ParseResult()
        node = res.register(self.statements())
        if res.error: return res
        return res.success(node)

    def arith_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = ArithOpNode(left, op_tok, right)

        return res.success(left)
    

# Parse Result
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register_backtrack(self):
        self.advance_count -= 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node
    
    def try_register(self, res):
        if res.error:
            self.to_reverse_count = self.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

from .values import Number, Function
from .errors import RuntimeError
from .tokentypes import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_INTDIV, TT_EXPO, TT_MOD, TT_GREATER, TT_LESS, TT_GREATEREQUAL, TT_LESSEQUAL, TT_EQUALTO, TT_NOTEQUAL, TT_NOT, TT_AND, TT_OR

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node, context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_DecimalNode(self, node, context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_BoolNode(self, node, context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_IdAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))
        
        if isinstance(value, Number):
            value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    
    def visit_IdAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_IntAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)
    
    def visit_FloatAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BoolAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)
    
    def visit_CharAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = node.value_node.value
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)
    
    def visit_StringAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = node.value_node.value
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)
        
    def visit_ArithOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multiplied_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.divided_by(right)
        elif node.op_tok.type == TT_INTDIV:
            result, error = left.intdivided_by(right)
        elif node.op_tok.type == TT_EXPO:
            result, error = left.raised_to(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.mod(right)
        elif node.op_tok.type == TT_GREATER:
            result, error = left.get_comp_greater(right)
        elif node.op_tok.type == TT_LESS:
            result, error = left.get_comp_less(right)
        elif node.op_tok.type == TT_GREATEREQUAL:
            result, error = left.get_comp_greaterequal(right)
        elif node.op_tok.type == TT_LESSEQUAL:
            result, error = left.get_comp_lessequal(right)
        elif node.op_tok.type == TT_EQUALTO:
            result, error = left.get_comp_equalto(right)
        elif node.op_tok.type == TT_NOTEQUAL:
            result, error = left.get_comp_notequal(right)
        elif node.op_tok.type == TT_AND:
            result, error = left.get_comp_and(right)
        elif node.op_tok.type == TT_OR:
            result, error = left.get_comp_or(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == TT_PLUS:
            number, error = number.multiplied_by(Number(1))
        elif node.op_tok.type == TT_MINUS:
            number, error = number.multiplied_by(Number(-1))
        elif node.op_tok.type == TT_NOT:
            number, error = number.get_comp_not()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
        
    def visit_IncrementNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))
        
        if isinstance(value, Number):
            value = value.copy().set_pos(node.pos_start, node.pos_end)

        error = None

        if node.op_tok1.type == TT_PLUS and node.op_tok2.type == TT_PLUS:
            value, error = value.added_to(Number(1))
        elif node.op_tok2.type == TT_MINUS and node.op_tok2.type == TT_MINUS:
            value, error = value.subbed_by(Number(1))

        if error:
            return res.failure(error)
        else:
            context.symbol_table.set(var_name, value)
            return res.success(value.set_pos(node.pos_start, node.pos_end))
        
    def visit_AskNode(self, node, context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)
            
        if node.more_case:
            more_value = res.register(self.visit(node.more_case, context))
            if res.error: return res
            return res.success(more_value)
        
        return res.success(None)
    
    def visit_RepeatNode(self, node, context):
        res = RTResult()

        var_name = node.var_name_tok.value
        try:
            context.symbol_table.remove(var_name)
        except(KeyError):
            pass
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        
        cond = res.register(self.visit(node.cond_node, context))
        if res.error: return res

        while cond.is_true():
            res.register(self.visit(node.body_node, context))
            if res.error: return res

            value = res.register(self.visit(node.iter_node, context))
            if res.error: return res

            cond = res.register(self.visit(node.cond_node, context))
            if res.error: return res

            context.symbol_table.set(var_name, value)

        return res.success(None)
    
    def visit_WhileNode(self, node, context):
        res = RTResult()

        while True:
            condition = res.register(self.visit(node.cond_node, context))
            if res.error: return res

            if not condition.is_true(): break

            res.register(self.visit(node.body_node, context))
            if res.error: return res

        return res.success(None)
    
    def visit_BuildDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)
    
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res

        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return res.success(return_value)

    
# Runtime Result

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self
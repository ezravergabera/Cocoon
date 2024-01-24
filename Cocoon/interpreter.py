from .errors import RuntimeError
from .tokentypes import TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_INTDIV, TT_EXPO, TT_MOD, TT_GREATER, TT_LESS, TT_GREATEREQUAL, TT_LESSEQUAL, TT_EQUALTO, TT_NOTEQUAL, TT_NOT, TT_AND, TT_OR
from .context import Context
from .symbolTable import SymbolTable
from .nodes import AskNode

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
        return RTResult().success(Float(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_BoolNode(self, node, context):
        return RTResult().success(Bool(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_StringNode(self, node, context):
        return RTResult().success(String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_CharNode(self, node, context):
        return RTResult().success(Character(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_UndefinedNode(self, node, context):
        return RTResult().success(Undefined(node.tok).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res

        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_numDeclareNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        in_symbolTable = context.symbol_table.hasValue(var_name)
        value = res.register(self.visit(node.value_node, context))

        if in_symbolTable:
            past_value = context.symbol_table.get(var_name)
            if not (type(value) == type(past_value)):
                return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"Data type mismatch",
                context
            ))
            else:
                return res.failure(RuntimeError(
                    node.pos_start, node.pos_end,
                    f"'{var_name}' is already defined",
                    context
                ))

        context.symbol_table.set(var_name, value)

        return res.success(None)

    def visit_deciDeclareNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        in_symbolTable = context.symbol_table.hasValue(var_name)
        value = res.register(self.visit(node.value_node, context))

        if in_symbolTable:
            past_value = context.symbol_table.get(var_name)
            if not (type(value) == type(past_value)):
                return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"Data type mismatch",
                context
            ))
            else:
                return res.failure(RuntimeError(
                    node.pos_start, node.pos_end,
                    f"'{var_name}' is already defined",
                    context
                ))

        context.symbol_table.set(var_name, value)

        return res.success(None)

    def visit_boolDeclareNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        in_symbolTable = context.symbol_table.hasValue(var_name)
        value = res.register(self.visit(node.value_node, context))

        if in_symbolTable:
            past_value = context.symbol_table.get(var_name)
            if not (type(value) == type(past_value)):
                return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"Data type mismatch",
                context
            ))
            else:
                return res.failure(RuntimeError(
                    node.pos_start, node.pos_end,
                    f"'{var_name}' is already defined",
                    context
                ))

        context.symbol_table.set(var_name, value)

        return res.success(None)

    def visit_charDeclareNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        in_symbolTable = context.symbol_table.hasValue(var_name)
        value = res.register(self.visit(node.value_node, context))

        if in_symbolTable:
            past_value = context.symbol_table.get(var_name)
            if not (type(value) == type(past_value)):
                return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"Data type mismatch",
                context
            ))
            else:
                return res.failure(RuntimeError(
                    node.pos_start, node.pos_end,
                    f"'{var_name}' is already defined",
                    context
                ))

        context.symbol_table.set(var_name, value)

        return res.success(None)

    def visit_textDeclareNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        in_symbolTable = context.symbol_table.hasValue(var_name)
        value = res.register(self.visit(node.value_node, context))

        if in_symbolTable:
            past_value = context.symbol_table.get(var_name)
            if not (type(value) == type(past_value)):
                return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"Data type mismatch",
                context
            ))
            else:
                return res.failure(RuntimeError(
                    node.pos_start, node.pos_end,
                    f"'{var_name}' is already defined",
                    context
                ))

        context.symbol_table.set(var_name, value)

        return res.success(None)

    def visit_IdAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if (type(value) == Undefined) or not value:
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is undefined\nDid you forgot to add a data type?",
                context
            ))
        
        if isinstance(value, Number):
            value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    
    def visit_IdAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        in_symbolTable = context.symbol_table.hasValue(var_name)
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        if not in_symbolTable and not isinstance(value, List) and not isinstance(node.value_node, AskNode):
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"{var_name} is undefined",
                context
            ))
        
        if in_symbolTable:
            past_value = context.symbol_table.get(var_name)
            if type(past_value) == Undefined:
                pass
            elif not (type(value) == type(past_value)):
                return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                f"Data type mismatch",
                context
            ))
        
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
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)
    
    def visit_StringAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
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
                f"'{var_name}' is undefined",
                context
            ))
        
        if isinstance(value, Number):
            value = value.copy().set_pos(node.pos_start, node.pos_end)
        elif isinstance(value, Float):
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                "Data type mismatch\nFloat cannot be incremented.",
                context
            ))
        else:
            return res.failure(RuntimeError(
                node.pos_start, node.pos_end,
                "Data type mismatch",
                context
            ))

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

        for condition, expr, should_return_empty in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(Number.empty if should_return_empty else expr_value)
            
        if node.more_case:
            expr, should_return_empty = node.more_case
            more_value = res.register(self.visit(expr, context))
            if res.error: return res
            return res.success(Number.empty if should_return_empty else more_value)
        
        return res.success(Number.empty)
    
    def visit_RepeatNode(self, node, context):
        res = RTResult()
        elements = []

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
            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res

            value = res.register(self.visit(node.iter_node, context))
            if res.error: return res

            cond = res.register(self.visit(node.cond_node, context))
            if res.error: return res

            context.symbol_table.set(var_name, value)

        return res.success(
            Number.empty if node.should_return_empty else 
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.cond_node, context))
            if res.error: return res

            if not condition.is_true(): break

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res

        return res.success(
            Number.empty if node.should_return_empty else 
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_BuildDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_return_empty).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)
    
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res

        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end).set_context(context)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
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
    
# Values
    
class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multiplied_by(self, other):
        return None, self.illegal_operation(other)

    def divided_by(self, other):
        return None, self.illegal_operation(other)

    def intdivided_by(self, other):
        return None, self.illegal_operation(other)

    def raised_to(self, other):
        return None, self.illegal_operation(other)

    def modulo(self, other):
        return None, self.illegal_operation(other)

    def get_comp_greater(self, other):
        return None, self.illegal_operation(other)

    def get_comp_less(self, other):
        return None, self.illegal_operation(other)

    def get_comp_greaterequal(self, other):
        return None, self.illegal_operation(other)

    def get_comp_lessequal(self, other):
        return None, self.illegal_operation(other)

    def get_comp_equalto(self, other):
        return None, self.illegal_operation(other)

    def get_comp_notequal(self, other):
        return None, self.illegal_operation(other)

    def get_comp_not(self):
        return None, self.illegal_operation()

    def get_comp_and(self, other):
        return None, self.illegal_operation(other)

    def get_comp_or(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RuntimeError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )

class Undefined(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def copy(self):
        raise Exception("No value defined")
    
    def __str__(self):
        return 'Undefined'

    def __repr__(self):
        return 'Undefined'

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(other.pos_start, other.pos_end, "Division by zero", self.context)
            
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def intdivided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(other.pos_start, other.pos_end, "Division by zero", self.context)
            
            return Number(self.value // other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def raised_to(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def modulo(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_greater(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_less(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_greaterequal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_lessequal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_equalto(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_notequal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_not(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
        
    def get_comp_and(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_or(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value != 0
        
    def __repr__(self):
        return str(self.value)
    
Number.empty = Number(0)

class Float(Number):
    def __init__(self, value):
        super().__init__(value)

class Bool(Number):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        if self.value == 1:
            return 'true'
        elif self.value == 0:
            return 'false'

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comp_equalto(self, other):
        if isinstance(other, String):
            return Bool(self.value == other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'"{self.value}"'
    
class Character(String):
    def __repr__(self):
        return f"'{self.value}'"
    
class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
    
    def added_to(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)
        
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f'{", ".join(str(x) for x in self.elements)}'

    def __repr__(self):
        return f'[{", ".join(str(x) for x in self.elements)}]'
    
class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    
    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RuntimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into '{self.name}'",
                self.context
            ))
        
        if len(args) < len(arg_names):
            return res.failure(RuntimeError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))
        
        return res.success(None)
    
    def populate_args(self, arg_names, args, exec_ctx):
        for argIdx in range(len(args)):
            arg_name = arg_names[argIdx]
            arg_value = args[argIdx]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()

        res.register(self.check_args(arg_names, args))
        if res.error: return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_return_empty):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_return_empty = should_return_empty

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.error: return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.error: return res
        return res.success(Number.empty if self.should_return_empty else value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_return_empty)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<build {self.name}>"
    
class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    
    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.error: return res

        return_value = res.register(method(exec_ctx))
        if res.error: return res
        return res.success(return_value)
    
    def no_visit_method(self, node, context):
        raise Exception(f"No execute_{self.name} method defined")
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
    def __repr__(self):
        return f"<built-in build {self.name}>"
    
    def execute_show(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_show.arg_names = ['value']

    def execute_get(self, exec_ctx):
        text = input()
        number = False
        try:
            number = int(text)
        except ValueError:
            text = str(text)
        if number:
            return RTResult().success(Number(number))
        elif text == 'true' or text == 'false':
            return RTResult().success(Bool(text))
        elif len(text) == 1:
            return RTResult().success(Character(text))
        return RTResult().success(String(text))
    execute_get.arg_names = []

BuiltInFunction.show    = BuiltInFunction("show")
BuiltInFunction.get     = BuiltInFunction("get")
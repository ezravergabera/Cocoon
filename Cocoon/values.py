from .errors import RuntimeError
from .interpreter import RTResult, Interpreter
from .context import Context
from .symbolTable import SymbolTable

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

class Number(Value):
    def __init__(self, value):
        self.value = value
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
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(other.pos_start, other.pos_end, "Division by zero", self.context)
            
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def intdivided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(other.pos_start, other.pos_end, "Division by zero", self.context)
            
            return Number(self.value // other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def raised_to(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)

    def modulo(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_greater(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_less(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_greaterequal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_lessequal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_equalto(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_notequal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_not(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
        
    def get_comp_and(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_comp_or(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def is_true(self):
        return self.value != 0
        
    def __repr__(self):
        return str(self.value)
    
class Function(Value):
    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) > len(self.arg_names):
            return res.failure(RuntimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_names)} too many args passed into '{self.name}'",
                self.context
            ))
        
        if len(args) < len(self.arg_names):
            return res.failure(RuntimeError(
                self.pos_start, self.pos_end,
                f"{len(self.arg_names) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))

        for argIdx in range(len(args)):
            arg_name = self.arg_names[argIdx]
            arg_value = self.args[argIdx]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error: return res
        return res.success(value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def repr(self):
        return f"<build {self.name}>"



class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end

    def added_to(self, other):
        if isinstance(other, Number):
            return (self.value + other.value)
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            return (self.value - other.value)
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return (self.value * other.value)
        
    def divided_by(self, other):
        if isinstance(other, Number):
            return (self.value / other.value)
        
    def intdivided_by(self, other):
        if isinstance(other, Number):
            return (self.value // other.value)
        
    def raised_to(self, other):
        if isinstance(other, Number):
            return (self.value ** other.value)

    def modulo(self, other):
        if isinstance(other, Number):
            return (self.value % other.value)
        
    def __repr__(self):
        return str(self.value)


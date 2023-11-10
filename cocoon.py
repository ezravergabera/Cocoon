# CONSTANTS

DIGITS = '0123456789'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
WHITESPACES = ' \t\n\v\r'
SPECIALCHARS = '%=~<>_&()[].!^"\',:;@?'
PUNCTUATIONS = '()[]'

# ERRORS

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class SyntaxError(Error):        # di pa gamit
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Syntax Error', details)

# POSITION

class Position:
    def __init__(self, idx, ln, col, fn, ftext):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftext = ftext

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftext)

# TOKENS (TT means token type)

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STR = 'TEXT'
TT_BOOL = 'BOOL'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MODULO'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_UNARY = 'Unary_Operator'
TT_OP = 'Arithmetic_Operator'
TT_ASSIGN = 'Assignment_Operator'
TT_ID = 'IDENTIFIER'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'

# LEXER

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in WHITESPACES:
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char in ALPHABET:
                tokens.append(self.make_identifier())
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char in PUNCTUATIONS:
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_ASSIGN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
            
        return tokens, None
    
    def make_punctuation(self):
        punctuation = ''

        if self.current_char in PUNCTUATIONS:
            if self.current_char == '(':
                punctuation += self.current_char
            elif self.current_char == ')':
                punctuation += self.current_char
            elif self.current_char == '[':
                punctuation += self.current_char

    def make_identifier(self):
        id_str = ''

        while self.current_char != None and self.current_char in ALPHABET + WHITESPACES:
            if self.current_char in WHITESPACES:
                break
            else:
                id_str += self.current_char
            self.advance()

        return Token(TT_ID, id_str)

    def make_string(self):
        text_str = ''
        q_count = 0

        while self.current_char != None and self.current_char in ALPHABET + WHITESPACES + '"':
            if self.current_char == '"':
                if q_count == 2:
                    break
                q_count += 1
                text_str += '"'
            else:
                text_str += self.current_char
            self.advance()

        return Token(TT_STR, text_str)

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

# RUN

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
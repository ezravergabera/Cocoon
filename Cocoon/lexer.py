from .constants import ALPHABET, DIGITS, WHITESPACES, OPERATORS, UNARY, RELATIONAL, LOGICAL, PUNCTUATIONS, CONSTANTS, KEYWORDS, NOISEWORDS, RESERVEDWORDS, UNTRACKED, INVALID
from .errors import Error, IllegalCharError, IllegalIdentifierError, IllegalNumberError, LexicalError, InvalidDecimalError, InvalidRelationalSymbol, ReferenceError
from .position import Position
from .tokens import Token
from .tokentypes import TT_ID, TT_ASSIGN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_INTDIV, TT_EXPO, TT_MOD, TT_INCRE, TT_DECRE, TT_POSITIVE, TT_NEGATIVE, TT_GREATER, TT_LESS, TT_GREATEREQUAL, TT_LESSEQUAL, TT_EQUALTO, TT_NOTEQUAL, TT_NOT, TT_AND, TT_OR, TT_INT, TT_FLOAT, TT_STR, TT_BOOL, TT_DTYPE, TT_KWORD, TT_RWORD, TT_NWORD, TT_COMMENT, TT_DOT, TT_COMMA, TT_SEMICOLON, TT_LSQUARE, TT_RSQUARE, TT_LPAREN, TT_RPAREN, TT_EOF

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    # Scan Character Method
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    # Look-Ahead Method
    def check(self):
        try:
            char = self.text[self.pos.idx + 1] if self.pos.idx < len(self.text) else None
        except IndexError:
            char = ''
        return char if char is not None else ''
    
    # Look-Behind Method
    def backtrack(self):
        try:
            char = self.text[self.pos.idx - 1] if self.pos.idx > 0 else None
        except IndexError:
            char = ''     
        return char if char is not None else ''

    # Tokenization Method
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            check = self.check()
            
            # Skips through whitespaces
            if self.current_char in WHITESPACES:
                self.advance()

            # Scans constants, keywords, reserved words, noise words, logical, and identifiers
            elif self.current_char in ALPHABET + '_':
                result = self.make_identifier()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result

            # Scans arithmetic operators: +, -, *, /, ~, ^, % and unary operators: +, -, ++, --
            elif self.current_char in OPERATORS:
                result = self.make_operator()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for single line comment and multiline comment
            elif self.current_char == '.' and check == '.' and check not in WHITESPACES:
                result = self.make_comments()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for number and decimal lexemes
            elif self.current_char in DIGITS + '.':
                result = self.make_number()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for invalid relational symbols such as !, &, |, &&, and ||
            elif (self.current_char in INVALID and check in WHITESPACES) or (self.current_char in INVALID and self.current_char == check):
                return [], self.invalid_relational()

            # Scans for assignment operator and relational lexemes
            elif self.current_char in RELATIONAL:
                result = self.make_relational()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for string literals enclosed with " or '
            elif self.current_char == '"' or self.current_char == "'":
                result = self.make_string()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for puntuations such as ., ,, ;, [, ], (, and )
            elif self.current_char in PUNCTUATIONS:
                tokens.append(self.make_punctuation())
                self.advance()

            # Returns an error when an invalid character is scanned
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        
        # End of File
        tokens.append(Token('TT_EOF', TT_EOF))
        return tokens, None
    
    # Scanner Methods
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        isUntracked = False

        while self.current_char != None and self.current_char in ALPHABET + DIGITS + WHITESPACES + '_' + UNTRACKED:
            if self.current_char in WHITESPACES:
                break
            elif self.current_char in UNTRACKED:
                isUntracked = True
                id_str += self.current_char
            else:
                id_str += self.current_char
            self.advance()

        if id_str == 'exit' and self.fn != "<stdin>":
            return ReferenceError(pos_start, self.pos, 'Usage of a reserved word.')
        elif id_str == 'exit':
            exit()

        if id_str in CONSTANTS:
            return Token(TT_DTYPE, id_str)
        elif id_str in KEYWORDS:
            return Token(TT_KWORD, id_str)
        elif id_str == 'true' or id_str == 'false':
            return Token(TT_BOOL, id_str)
        elif id_str in RESERVEDWORDS:
            return Token(TT_RWORD, id_str)
        elif id_str in NOISEWORDS:
            return Token(TT_NWORD, id_str)
        elif id_str in LOGICAL:
            return self.make_logical(id_str)
        elif isUntracked == True:
            return IllegalIdentifierError(pos_start, self.pos, f'{id_str}')
        else:
            return Token(TT_ID, id_str)
        
    def make_logical(self, log_str):
        if log_str == 'NOT' or log_str == 'not':
            return Token(TT_NOT, log_str)
        elif log_str == 'AND' or log_str == 'and':
            return Token(TT_AND, log_str)
        elif log_str == 'OR' or log_str == 'or':
            return Token(TT_OR, log_str)
        else:
            # for future if magkaerror man in this part
            print("HALA MAY ERROR SA MAKE_LOGICAL")

    def make_comments(self):
        pos_start = self.pos.copy()
        comment_str = ''
        comment_str += self.current_char
        self.advance()
        check = self.check()
        dot_count = 0
        
        if self.current_char == '.' and check == '.' and check not in WHITESPACES:
            while dot_count != 3:
                comment_str += self.current_char
                if self.check() == '' and self.check() != None:
                    return LexicalError(pos_start, self.pos, 'Closing symbol not found.')
                
                if self.current_char == '.':
                    dot_count += 1
                else:
                    dot_count = 0
                self.advance()
        else:
            comment_str += self.current_char
            self.advance()
            while self.current_char != '\n' and self.current_char != None:
                comment_str += self.current_char
                self.advance()
                
        if self.current_char == '\n':
            self.advance()

        return Token(TT_COMMENT, comment_str)
    
    def make_operator(self):
        operator = ''

        result = self.make_unary()
        if isinstance(result, Token):
            return result
        
        operator += self.current_char
        self.advance()

        if operator == '+':
            return Token(TT_PLUS, operator)
        elif operator == '-':
            return Token(TT_MINUS, operator)
        elif operator == '*':
            return Token(TT_MUL, operator)
        elif operator == '/':
            return Token(TT_DIV, operator)
        elif operator == '~':
            return Token(TT_INTDIV, operator)
        elif operator == '^':
            return Token(TT_EXPO, operator)
        elif operator == '%':
            return Token(TT_MOD, operator)

    def make_unary(self):
        unary_str = ''
        check = self.check()
        backtrack = self.backtrack()

        if self.current_char != None and self.current_char in UNARY:

            # For scanning increments and decrements. 2 characters
            if self.current_char == '+' and self.current_char == check and backtrack in WHITESPACES:
                unary_str += self.current_char
                self.advance()
                unary_str += self.current_char
                self.advance()
                return Token(TT_INCRE, unary_str)
            elif self.current_char == '-' and self.current_char == check and backtrack in WHITESPACES:
                unary_str += self.current_char
                self.advance()
                unary_str += self.current_char
                self.advance()
                return Token(TT_DECRE, unary_str)
            elif self.current_char == '+' and self.current_char == check and backtrack in ALPHABET + DIGITS:
                unary_str += self.current_char
                self.advance()
                unary_str += self.current_char
                self.advance()
                return Token(TT_INCRE, unary_str)
            elif self.current_char == '-' and self.current_char == check and backtrack in ALPHABET + DIGITS:
                unary_str += self.current_char
                self.advance()
                unary_str += self.current_char
                self.advance()
                return Token(TT_DECRE, unary_str)

            # For scanning positive and negative unary. 1 character
            if self.current_char == '+' and check in ALPHABET + DIGITS and (backtrack not in ALPHABET + DIGITS + OPERATORS or backtrack in WHITESPACES):
                unary_str += self.current_char
                self.advance()
                return Token(TT_POSITIVE, unary_str)
            elif self.current_char == '-' and check in ALPHABET + DIGITS and (backtrack not in ALPHABET + DIGITS + OPERATORS or backtrack in WHITESPACES):
                unary_str += self.current_char
                self.advance()
                return Token(TT_NEGATIVE, unary_str)

    def make_number(self):
        num_str = ''
        dot_count = 0
        isValid = True
        isIdentifier = False
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ALPHABET + WHITESPACES + '.' + UNTRACKED + '_':
            check = self.check()

            if self.current_char in WHITESPACES:
                break
            elif num_str and self.current_char == '_' and check == '_' or isValid == False:
                isValid = False
                num_str += self.current_char
            elif self.current_char in ALPHABET + UNTRACKED:
                isValid = False
                num_str += self.current_char
            elif (not num_str and self.current_char in DIGITS) and check in ALPHABET and check not in WHITESPACES:
                isIdentifier = True
                num_str += self.current_char
            elif self.current_char == '.':
                if dot_count == 1:
                    dot_count += 1
                dot_count += 1
                num_str += '.'
            else:
                if self.current_char != '_':
                    num_str += self.current_char
            self.advance()

        if dot_count == 0 and isValid == True and isIdentifier == False:
            return Token(TT_INT, int(num_str))
        elif dot_count == 2 and isValid == True:
            return LexicalError(pos_start, self.pos, f'{num_str}')
        elif isIdentifier:
            return IllegalIdentifierError(pos_start, self.pos, f'{num_str}')
        elif isValid == False:
            return IllegalNumberError(pos_start, self.pos, f'{num_str}')
        elif num_str == '.':
            return Token(TT_DOT, num_str)
        else:
            try:
                return Token(TT_FLOAT, float(num_str))
            except ValueError:
                return InvalidDecimalError(pos_start, self.pos, "Invalid Decimal")

    def invalid_relational(self):
        rel_str = ''

        while self.current_char != None and self.current_char in INVALID:
            check = self.check()
            rel_str += self.current_char
            pos_start = self.pos.copy()

            if rel_str == '!' and check in WHITESPACES:
                self.advance()
                return InvalidRelationalSymbol(pos_start, self.pos, f'"{rel_str}", Consider using "not" or "NOT" instead.')
            elif rel_str == '&' and check in WHITESPACES:
                self.advance()
                return InvalidRelationalSymbol(pos_start, self.pos, f'"{rel_str}", Consider using "and" or "AND" instead.')
            elif rel_str == '|' and check in WHITESPACES:
                self.advance()
                return InvalidRelationalSymbol(pos_start, self.pos, f'"{rel_str}", Consider using "or" or "OR" instead.')
            elif rel_str == '&' and check == '&':
                self.advance()
                rel_str += self.current_char
                self.advance()
                return InvalidRelationalSymbol(pos_start, self.pos, f'"{rel_str}", Consider using "and" or "AND" instead.')
            elif rel_str == '|' and check == '|':
                self.advance()
                rel_str += self.current_char
                self.advance()
                return InvalidRelationalSymbol(pos_start, self.pos, f'"{rel_str}", Consider using "or" or "OR" instead.')
            else:
                self.advance()
                return IllegalCharError(pos_start, self.pos, f"'{self.current_char}'")

    def make_relational(self):
        rel_str = ''
        check = self.check()

        if self.current_char == '=' and check != '=':
            rel_str += self.current_char
            self.advance()
            return Token(TT_ASSIGN, rel_str)
        elif self.current_char == '>' and check == '=':
            rel_str += self.current_char
            self.advance()
            rel_str += self.current_char
            self.advance()
            return Token(TT_GREATEREQUAL, rel_str)
        elif self.current_char == '<' and check == '=':
            rel_str += self.current_char
            self.advance()
            rel_str += self.current_char
            self.advance()
            return Token(TT_LESSEQUAL, rel_str)
        elif self.current_char == '=' and check == '=':
            rel_str += self.current_char
            self.advance()
            rel_str += self.current_char
            self.advance()
            return Token(TT_EQUALTO, rel_str)
        elif self.current_char == '!' and check == '=':
            rel_str += self.current_char
            self.advance()
            rel_str += self.current_char
            self.advance()
            return Token(TT_NOTEQUAL, rel_str)
        elif self.current_char == '>':
            rel_str += self.current_char
            self.advance()
            return Token(TT_GREATER, rel_str)
        elif self.current_char == '<':
            rel_str += self.current_char
            self.advance()
            return Token(TT_LESS, rel_str)

    def make_string(self):
        text_str = ''
        stop = self.current_char
        text_str += stop
        pos_start = self.pos.copy()
        self.advance()

        while self.current_char != None and self.current_char != stop:
            text_str += self.current_char
            self.advance()
        
        if self.current_char == '"' or self.current_char == "'":
            text_str += stop
            self.advance()
        else:
            return LexicalError(pos_start, self.pos, "Must be enclosed by \" or \'.")
        return Token(TT_STR, text_str)

    def make_punctuation(self):
        if self.current_char in PUNCTUATIONS:
            char = self.current_char
            if char == '.':
                return Token(TT_DOT, char)
            if char == ',':
                return Token(TT_COMMA, char)
            elif char == ';':
                return Token(TT_SEMICOLON, char)
            elif char == '[':
                return Token(TT_LSQUARE, char)
            elif char == ']':
                return Token(TT_RSQUARE, char)
            elif char == '(':
                return Token(TT_LPAREN, char)
            elif char == ')':
                return Token(TT_RPAREN, char)
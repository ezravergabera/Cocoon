from .check import *
from .errors import Error, IllegalCharError, IllegalIdentifierError, IllegalNumberError, LexicalError, InvalidDecimalError, InvalidRelationalSymbol, ReferenceError
from .position import Position
from .tokens import Token
from .tokentypes import TT_ID, TT_ASSIGN, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_INTDIV, TT_EXPO, TT_MOD, TT_GREATER, TT_LESS, TT_GREATEREQUAL, TT_LESSEQUAL, TT_EQUALTO, TT_NOTEQUAL, TT_NOT, TT_AND, TT_OR, TT_INT, TT_FLOAT, TT_STR, TT_BOOL, TT_CHAR, TT_DTYPE, TT_KWORD, TT_RWORD, TT_NWORD, TT_COMMENT, TT_DOT, TT_COMMA, TT_SEMICOLON, TT_LSQUARE, TT_RSQUARE, TT_LPAREN, TT_RPAREN, TT_EOF

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
            char = self.current_char
            check = self.check()
            
            # Skips through whitespaces
            if isWhitespace(char):
                self.advance()

            # Scans constants, keywords, reserved words, noise words, logical, and identifiers
            elif isAlphabet(char) or char == '_':
                result = self.make_identifier()
                if isinstance(result, Token): 
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result

            # Scans arithmetic operators: +, -, *, /, ~, ^, %, invalid relational symbols such as !, &, |, &&, and ||, and assignment operator and relational lexemes
            elif isOperator(char):
                result = self.make_operator()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for single line comment and multiline comment
            elif char == '.' and check == '.' and not isWhitespace(check):
                result = self.make_comments()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for number and decimal lexemes
            elif isDigits(char) or char == '.':
                result = self.make_number()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result
                
            # Scans for string literals enclosed with "
            elif char == '"':
                result = self.make_string()
                if isinstance(result, Token):
                    tokens.append(result)
                elif isinstance(result, Error):
                    return [], result

            #Scans for character lexemes    
            elif char == "'":
               result = self.make_char()
               if isinstance(result, Token):
                   tokens.append(result)
                   self.advance()
               elif isinstance(result, Error):
                   return[], result
            
                
            # Scans for puntuations such as ., ,, ;, [, ], (, and )
            elif isPunctuation(char):
                tokens.append(self.make_punctuation())
                self.advance()

            # Returns an error when an invalid character is scanned
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        
        # End of File
        tokens.append(Token('TT_EOF', TT_EOF, pos_start=self.pos))
        return tokens, None
    
    # Scanner Methods
    def make_identifier(self):
        lexeme = ''
        tokentype = TT_ID
        pos_start = self.pos.copy()

        while self.current_char != None and (isAlphabet(self.current_char) or isDigits(self.current_char) or isWhitespace(self.current_char) or isUntracked(self.current_char) or self.current_char == '_'):
            # Whitespaces
            if isWhitespace(self.current_char):
                break

            # AND
            elif self.current_char == 'A' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'N':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'D':
                        lexeme += self.current_char
                        tokentype = TT_AND
                        self.advance()

            # and, askmore
            elif self.current_char == 'a' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'n':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'd':
                        lexeme += self.current_char
                        tokentype = TT_AND
                        self.advance()
                # askmore
                elif self.current_char == 's':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'k':
                        lexeme += self.current_char
                        tokentype = TT_RWORD
                        self.advance()
                        if self.current_char == 'm':
                            lexeme += self.current_char
                            tokentype = TT_ID
                            self.advance()
                            if self.current_char == 'o':
                                lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'r':
                                    lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'e':
                                        lexeme += self.current_char
                                        tokentype = TT_RWORD
                                        self.advance()

            # boolean, build
            elif self.current_char == 'b' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                # bool
                if self.current_char == 'o':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'o':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'l':
                            lexeme += self.current_char
                            tokentype = TT_DTYPE
                            # boolean
                            self.advance()
                            if self.current_char == 'e':
                                lexeme += self.current_char
                                tokentype = TT_ID
                                self.advance()
                                if self.current_char == 'a':
                                    lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'n':
                                        lexeme += self.current_char
                                        tokentype = TT_DTYPE
                                        self.advance()
                # build
                elif self.current_char == 'u':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'i':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'l':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'd':
                                lexeme += self.current_char
                                tokentype = TT_RWORD
                                self.advance()

            # character
            elif self.current_char == 'c' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'h':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'a':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'r':
                            lexeme += self.current_char
                            tokentype = TT_DTYPE
                            self.advance()
                            if self.current_char == 'a':
                                lexeme += self.current_char
                                tokentype = TT_ID
                                self.advance()
                                if self.current_char == 'c':
                                    lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 't':
                                        lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 'e':
                                            lexeme += self.current_char
                                            self.advance()
                                            if self.current_char == 'r':
                                                lexeme += self.current_char
                                                tokentype = TT_DTYPE
                                                self.advance()

            # done, decimal
            elif self.current_char == 'd' and len(lexeme) == 0:
                # do
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'o':
                    lexeme += self.current_char
                    tokentype = TT_NWORD
                    self.advance()
                    # done
                    if self.current_char == 'n':
                        lexeme += self.current_char
                        tokentype = TT_ID
                        self.advance()
                        if self.current_char == 'e':
                            lexeme += self.current_char
                            tokentype = TT_RWORD
                            self.advance()
                # deci
                elif self.current_char == 'e':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'c':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'i':
                            lexeme += self.current_char
                            tokentype = TT_DTYPE
                            self.advance()
                            # decimal
                            if self.current_char == 'm':
                                lexeme += self.current_char
                                tokentype = TT_ID
                                self.advance()
                                if self.current_char == 'a':
                                    lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'l':
                                        lexeme += self.current_char
                                        tokentype = TT_DTYPE
                                        self.advance()

            # empty, exit, end, enough
            elif self.current_char == 'e' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                # empty
                if self.current_char == 'm':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'p':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 't':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'y':
                                lexeme += self.current_char
                                tokentype = TT_RWORD
                                self.advance()
                # exit and its function
                elif self.current_char == 'x':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'i':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 't':
                            lexeme += self.current_char
                            tokentype = TT_RWORD
                            self.advance()
                            if (isWhitespace(self.check()) or self.check() == None) and self.fn != "<stdin>":
                                return ReferenceError(pos_start, self.pos, 'Usage of a reserved word.')
                            elif isWhitespace(self.check()) or self.check() == None:
                                exit()
                # end
                elif self.current_char == 'n':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'd':
                        lexeme += self.current_char
                        tokentype = TT_NWORD
                        self.advance()
                    # enough
                    elif self.current_char == 'o':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'u':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'g':
                                lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'h':
                                    lexeme += self.current_char
                                    tokentype = TT_RWORD
                                    self.advance()

            # false                                    
            elif self.current_char == 'f' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'a':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'l':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 's':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'e':
                                lexeme += self.current_char
                                tokentype = TT_BOOL
                                self.advance()

            # get, give, group
            elif self.current_char == 'g' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 't':
                        lexeme += self.current_char
                        tokentype = TT_KWORD
                        self.advance()
                # give
                elif self.current_char == 'i':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'v':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            lexeme += self.current_char
                            tokentype = TT_RWORD
                            self.advance()
                # group
                elif self.current_char == 'r':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'o':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'u':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'p':
                                lexeme += self.current_char
                                tokentype = TT_RWORD
                                self.advance()

            # more
            elif self.current_char == 'm' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'o':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'r':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            lexeme += self.current_char
                            tokentype = TT_RWORD
                            self.advance()

            # NOT
            elif self.current_char == 'N' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'O':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'T':
                        lexeme += self.current_char
                        tokentype = TT_NOT
                        self.advance()

            # next, not, number
            elif self.current_char == 'n' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'x':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 't':
                            lexeme += self.current_char
                            tokentype = TT_RWORD
                            self.advance()
                # not
                elif self.current_char == 'o':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 't':
                        lexeme += self.current_char
                        tokentype = TT_NOT
                        self.advance()
                # num
                elif self.current_char == 'u':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'm':
                        lexeme += self.current_char
                        tokentype = TT_DTYPE
                        self.advance()
                        # number
                        if self.current_char == 'b':
                            lexeme += self.current_char
                            tokentype = TT_ID
                            self.advance()
                            if self.current_char == 'e':
                                lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'r':
                                    lexeme += self.current_char
                                    tokentype = TT_DTYPE
                                    self.advance()

            # OR
            elif self.current_char == 'O' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'R':
                    lexeme += self.current_char
                    tokentype = TT_OR
                    self.advance()

            # or
            elif self.current_char == 'o' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'r':
                    lexeme += self.current_char
                    tokentype = TT_OR
                    self.advance()

            # repeat, raising, raise
            elif self.current_char == 'r' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'p':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'a':
                                lexeme += self.current_char
                                self.advance()
                                if self.current_char == 't':
                                    lexeme += self.current_char
                                    tokentype = TT_RWORD
                                    self.advance()
                # raising
                elif self.current_char == 'a':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'i':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 's':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'i':
                                lexeme += self.current_char
                                self.advance()
                                if self.current_char == 'n':
                                    lexeme += self.current_char
                                    self.advance()
                                    if self.current_char == 'g':
                                        lexeme += self.current_char
                                        tokentype = TT_RWORD
                                        self.advance()
                            # raise
                            elif self.current_char == 'e':
                                lexeme += self.current_char
                                tokentype = TT_RWORD
                                self.advance()

            # show, start
            elif self.current_char == 's' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'h':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'o':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'w':
                            lexeme += self.current_char
                            tokentype = TT_KWORD
                            self.advance()
                # start
                elif self.current_char == 't':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'a':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'r':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 't':
                                lexeme += self.current_char
                                tokentype = TT_NWORD
                                self.advance()

            # text, true
            elif self.current_char == 't' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'e':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'x':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 't':
                            lexeme += self.current_char
                            tokentype = TT_DTYPE
                            self.advance()
                # true
                elif self.current_char == 'r':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'u':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            lexeme += self.current_char
                            tokentype = TT_BOOL
                            self.advance()

            # undef
            elif self.current_char == 'u' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'n':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'd':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'e':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char == 'f':
                                lexeme += self.current_char
                                tokentype = TT_RWORD
                                self.advance()
                                # undefined
                                if self.current_char == 'i':
                                    lexeme += self.current_char
                                    tokentype = TT_ID
                                    self.advance()
                                    if self.current_char == 'n':
                                        lexeme += self.current_char
                                        self.advance()
                                        if self.current_char == 'e':
                                            lexeme += self.current_char
                                            self.advance()
                                            if self.current_char == 'd':
                                                lexeme += self.current_char
                                                tokentype = TT_RWORD
                                                self.advance()

            # while
            elif self.current_char == 'w' and len(lexeme) == 0:
                lexeme += self.current_char
                self.advance()
                if self.current_char == 'h':
                    lexeme += self.current_char
                    self.advance()
                    if self.current_char == 'i':
                        lexeme += self.current_char
                        self.advance()
                        if self.current_char == 'l':
                            lexeme += self.current_char
                            self.advance()
                            if self.current_char =='e':
                                lexeme += self.current_char
                                tokentype = TT_RWORD
                                self.advance()

            # other identifiers
            else:
                lexeme += self.current_char
                tokentype = TT_ID
                self.advance()

        return Token(tokentype, lexeme, pos_start, self.pos)

    def make_comments(self):
        pos_start = self.pos.copy()
        comment_str = ''
        comment_str += self.current_char
        self.advance()
        check = self.check()
        dot_count = 0
        
        if self.current_char == '.' and check == '.':
            comment_str += self.current_char
            self.advance()
            comment_str += self.current_char
            self.advance()
            while dot_count != 3:
                if self.current_char == '.':
                    dot_count += 1
                else:
                    dot_count = 0

                if self.check() == '' or self.check() == None:
                    return LexicalError(pos_start, self.pos, 'Closing symbol not found.')
                
                comment_str += self.current_char
                self.advance()
        else:
            comment_str += self.current_char
            self.advance()
            while self.current_char != '\n' and self.current_char != None:
                comment_str += self.current_char
                self.advance()
                
            if self.current_char == '\n':
                self.advance()

        return Token(TT_COMMENT, comment_str, pos_start, self.pos)
    
    def make_operator(self):
        tokentype = ''
        lexeme = ''
        details = ''
        isTok = False
        isErr = False
        pos_start = self.pos.copy()

        if self.current_char == '+':
            tokentype = TT_PLUS
            lexeme += self.current_char
            isTok = True
            self.advance()
        elif self.current_char == '-':
            tokentype = TT_MINUS
            lexeme += self.current_char
            isTok = True
            self.advance()
        elif self.current_char == '*':
            tokentype = TT_MUL
            lexeme += self.current_char
            isTok = True
            self.advance()
        elif self.current_char == '/':
            tokentype = TT_DIV
            lexeme += self.current_char
            isTok = True
            self.advance()
        elif self.current_char == '~':
            tokentype = TT_INTDIV
            lexeme += self.current_char
            isTok = True
            self.advance()
        elif self.current_char == '^':
            tokentype = TT_EXPO
            lexeme += self.current_char
            isTok = True
            self.advance()
        elif self.current_char == '%':
            tokentype = TT_MOD
            lexeme += self.current_char
            isTok = True
            self.advance()
        elif self.current_char == '=':
            tokentype = TT_ASSIGN
            lexeme += self.current_char
            isTok = True
            self.advance()
            if self.current_char == '=':
                tokentype = TT_EQUALTO
                lexeme += self.current_char
                isTok = True
                self.advance()
        elif self.current_char == '>':
            tokentype = TT_GREATER
            lexeme += self.current_char
            isTok = True
            self.advance()
            if self.current_char == '=':
                tokentype = TT_GREATEREQUAL
                lexeme += self.current_char
                isTok = True
                self.advance()
        elif self.current_char == '<':
            tokentype = TT_LESS
            lexeme += self.current_char
            isTok = True
            self.advance()
            if self.current_char == '=':
                tokentype = TT_LESSEQUAL
                lexeme += self.current_char
                isTok = True
                self.advance()
        elif self.current_char == '!':
            lexeme += self.current_char
            details = f'"{lexeme}", Consider using "not" or "NOT" instead.'
            isErr = True
            self.advance()
            if self.current_char == '=':
                tokentype = TT_NOTEQUAL
                lexeme += self.current_char
                isTok = True
                isErr = False
                self.advance()
        elif self.current_char == '&':
            lexeme += self.current_char
            details = f'"{lexeme}", Consider using "and" or "AND" instead.'
            isErr = True
            self.advance()
            if self.current_char == '&':
                lexeme += self.current_char
                details = f'"{lexeme}", Consider using "and" or "AND" instead.'
                isErr = True
                self.advance()
        elif self.current_char == '|':
            lexeme += self.current_char
            details = f'"{lexeme}", Consider using "or" or "OR" instead.'
            isErr = True
            self.advance()
            if self.current_char == '|':
                lexeme += self.current_char
                details = f'"{lexeme}", Consider using "or" or "OR" instead.'
                isErr = True
                self.advance()

        if isTok:
            return Token(tokentype, lexeme, pos_start, self.pos)
        elif isErr:
            return InvalidRelationalSymbol(pos_start, self.pos, details)

    def make_number(self):
        pos_start = self.pos.copy()
        num_str = ''
        dot_count = 0
        isValid = True
        isIdentifier = False

        while self.current_char != None and (isAlphabet(self.current_char) or isDigits(self.current_char) or isWhitespace(self.current_char) or isUntracked(self.current_char) or self.current_char == '_' or self.current_char == '.'):
            check = self.check()

            if isWhitespace(self.current_char):
                break
            elif num_str and self.current_char == '_' and check == '_' or isValid == False:
                isValid = False
                num_str += self.current_char
            elif isAlphabet(self.current_char) or isUntracked(self.current_char):
                isValid = False
                num_str += self.current_char
            elif (not num_str and isDigits(self.current_char)) and isAlphabet(check) and not isWhitespace(check):
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
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        elif dot_count == 2 and isValid == True:
            return LexicalError(pos_start, self.pos, f'{num_str}')
        elif isIdentifier:
            return IllegalIdentifierError(pos_start, self.pos, f'{num_str}')
        elif isValid == False:
            return IllegalNumberError(pos_start, self.pos, f'{num_str}')
        elif num_str == '.':
            return Token(TT_DOT, num_str, pos_start, self.pos)
        else:
            try:
                return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
            except ValueError:
                return InvalidDecimalError(pos_start, self.pos, "Invalid Decimal")

    def make_string(self):
        pos_start = self.pos.copy()
        text_str = ''
        stop = self.current_char
        text_str += stop
        self.advance()

        while self.current_char != None and self.current_char != stop and isinCharSet(self.current_char):
            text_str += self.current_char
            self.advance()
        
        if self.current_char == stop:
            text_str += stop
            self.advance()
        else:
            if not(isinCharSet(self.current_char)):
                return LexicalError(pos_start, self.pos, f"'{self.current_char}' not in character_set")   
            return LexicalError(pos_start, self.pos, "Must be enclosed by \".")
        return Token(TT_STR, text_str, pos_start, self.pos)
    
    def make_char(self):
        pos_start = self.pos.copy()
        self.advance()
        if isAlphabet(self.current_char):
            char_value = self.current_char
            self.advance()
            if self.current_char == "'":
                return Token(TT_CHAR, char_value, self.pos)
            else:
                return LexicalError(pos_start, self.pos, "Must be enclosed by \'. ")
        else:
            return LexicalError(pos_start, self.pos, "Must be an Alphabet")

    def make_punctuation(self):
        if isPunctuation(self.current_char):
            char = self.current_char
            if char == '.':
                return Token(TT_DOT, char, self.pos)
            if char == ',':
                return Token(TT_COMMA, char, self.pos)
            elif char == ';':
                return Token(TT_SEMICOLON, char, self.pos)
            elif char == '[':
                return Token(TT_LSQUARE, char, self.pos)
            elif char == ']':
                return Token(TT_RSQUARE, char, self.pos)
            elif char == '(':
                return Token(TT_LPAREN, char, self.pos)
            elif char == ')':
                return Token(TT_RPAREN, char, self.pos)
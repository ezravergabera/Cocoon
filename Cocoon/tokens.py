class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def __str__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

    def __repr__(self, indent=0):
        if self.value:
            return f'{{\n{" " * (indent + 4)}token type: {self.type},\n{" " * (indent + 4)}token value: {self.value}\n{" " * indent}}}'
        return f'{{\n{" " * (indent + 4)}token type: {self.type}\n{" " * indent}}}'

    def matches(self, type_, value):
        return self.type == type_ and self.value == value


def tok_to_str(tokens):
    tok_str = ''

    if (tokens != None):
        for tok in tokens:
            if tok.value == '\n':
                tok_str += f'{tok.type: >20}    ' + '\\n\n'
            elif tok.value:
                tok_str += f'{tok.type: >20}    {tok.value}\n'
            else:
                tok_str += f'{str(tok.type): >20}    {tok.type}\n'

    return tok_str


def output_to_symbolTable(fn, tokens):
    filename = 'symbolTable.txt'

    with open(filename, "w") as f:
        f.write(f'{"File name:": >20}    {fn}\n')
        f.write(f'{"TOKENS": >20}    LEXEMES\n')
        f.write('----------------------------------------\n')
        f.write(tok_to_str(tokens))

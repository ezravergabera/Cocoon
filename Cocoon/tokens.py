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

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
    def matches(self, type_, value):
        return self.type == type_ and self.value == value


def tok_to_str(tokens):
    tok_str = ''

    if(tokens != None):
        for tok in tokens:
            if tok.value:
                tok_str += f'{tok.type: >20}    {tok.value}\n'
            else:
                tok_str += f'{str(tok.type): >20}    {tok.type}\n'

    return tok_str

def print_tokens(fn, tokens):
    text = ''
    text += (f'{"File name:": >20}    {fn}\n')
    text += (f'{"TOKENS": >20}    LEXEMES\n')
    text += ('----------------------------------------\n')
    text += (tok_to_str(tokens))

    return text

def output_to_symbolTable(tokens):
    filename = 'symbolTable.txt'

    with open(filename, "w") as f:
        f.write(f'{"File name:": >20}    {filename}\n')
        f.write(f'{"TOKENS": >20}    LEXEMES\n')
        f.write('----------------------------------------\n')
        f.write(tok_to_str(tokens))
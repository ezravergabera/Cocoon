from Cocoon.lexer import Lexer
from Cocoon.parser import Parser
from Cocoon.interpreter import *
from Cocoon.context import Context
from Cocoon.symbolTable import SymbolTable
from Cocoon.tokens import tok_to_str, output_to_symbolTable
import sys

debugmode = False

# Global Symbol Table
global_symbol_table = SymbolTable()
global_symbol_table.set('empty', Number.empty)
global_symbol_table.set('show', BuiltInFunction.show)
global_symbol_table.set('get', BuiltInFunction.get)

def debug_lexer():
    debugmode = True
    while True:
        text = input("lexer > ")
        if text.strip() == "": continue
        result, error, _ = run_lexer("<stdin>", text)

        if error:
            try:
                for err in error:
                    print(err.as_string())
            except(TypeError):
                print(error.as_string())
        elif result:
            output_to_symbolTable(result)
            result.pop()
            print(repr(result))

def debug_parser():
    debugmode = True
    while True:
        text = input("parser > ")
        if text.strip() == "": continue
        result, error, _ = run_parser("<stdin>", text)

        if error: 
            try:
                for err in error:
                    print(err.as_string())
            except(TypeError):
                print(error.as_string())
        elif result: print(repr(result))

def debug_interpreter():
    debugmode = True
    while True:
        text = input("interpreter > ")
        if text.strip() == "": continue
        result, error, _, __ = run_interpreter("<stdin>", text)

        if error: 
            try:
                for err in error:
                    print(err.as_string())
            except(TypeError):
                print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))

def run_lexer(fn, text):
    # Lexer
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error

def run_parser(fn, text):
    # Lexer
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    # Parser
    if error: return None, error, None

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error, tokens

def run_interpreter(fn, text):
    # Lexer
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    # Parser
    if error: return None, error, None

    parser = Parser(tokens)
    ast = parser.parse()

    # Interpreter
    if ast.error: return None, ast.error, None

    interpreter = Interpreter()
    # Context Initial route
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error, tokens, ast.node

def run(fn, text):
    # Lexer
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    # return tokens, error

    # Parser
    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    # return ast.node, ast.error

    # Interpreter
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    # Context Initial route
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

def print_tokens(fn, tokens):
    text = ''
    text += f'{"File name:": >20}    {fn}\n'
    text += f'{"TOKENS": >20}    LEXEMES\n'
    text += '----------------------------------------\n'
    text += tok_to_str(tokens)

    return text

def print_ast(fn, ast):
    text = ''
    text += f'File name:    {fn}\n'
    text += "Abstract Syntax Tree:\n"
    text += f'{repr(ast)}\n'

    return text

def print_res(fn, res):
    text = ''
    text += f'File name:    {fn}\n'
    text += "Result:\n"
    result = str(res).split(", ")
    for resout in result:
        text += f'{" ": >5}{resout}\n'

    return text

def output_to_syntacticTable(fn, ast):
    filename = 'syntacticTable.txt'

    with open(filename, "w") as f:
        f.write(f'File name:    {fn}\n')
        f.write("Abstract Syntax Tree:\n")
        f.write(repr(ast))

#* For Debugging
# debug_lexer()
# debug_parser()
# debug_interpreter()


# Run File Command
def run_file(filename):
    if(filename):
        if(filename.lower().endswith('.kkun')):
            try:
                with open(filename, 'r') as f:
                    text = f.read()
                
                result, error, tokens, ast = run_interpreter(filename, text)

                print_tokens(filename, tokens)
                print_ast(filename, ast)
                print_res(filename, result)
                output_to_symbolTable(result)
                output_to_syntacticTable(ast)

                if error:
                    try:
                        for err in error:
                            print(err.as_string())
                    except(TypeError):
                        print(error.as_string())
            except FileNotFoundError:
                print("File does not exist!")
        else:
            print("Invalid file name extension!")


# Shell Commands
OPTIONS = {'-f', '-file', '-c', 'cli'}
lowercasedArgs = [arg.lower() for arg in sys.argv]

if __name__ == '__main__' and debugmode == False:
    if '-cli' in lowercasedArgs or '-c' in lowercasedArgs:
        while True:
            text = input("cocoon > ")

            result, error = run_lexer("<stdin>", text)

            if error:
                print(error.as_string())
            elif result:
                output_to_symbolTable(result)
                result.pop()
                print(result)
    elif '-file' in lowercasedArgs or '-f' in lowercasedArgs:
        if '-f' in lowercasedArgs:
            flagidx = lowercasedArgs.index('-f') 
        elif '-file' in lowercasedArgs:
            flagidx = lowercasedArgs.index('-file')
        try:
            run_file(sys.argv[flagidx + 1])
        except IndexError:
            print("No file name argument is found!")
    else:
        try:
            print(sys.argv)
            if len(sys.argv) <= 2:
                print(f'Unknown option: {sys.argv[1]}')
                print('usage: python shell.py [option] ... [-cli | -c] | ([-file | -f] [arg])')
            elif len(sys.argv) >= 3:
                print(f'SyntaxError: No valid option found!')
                print('usage: python shell.py [option] ... [-cli | -c] | ([-file | -f] [arg])')
        except IndexError:
            print('No valid argument found!')

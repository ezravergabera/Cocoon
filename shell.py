from Cocoon.lexer import Lexer
from Cocoon.parser import Parser
from Cocoon.interpreter import Interpreter
from Cocoon.tokens import tok_to_str, output_to_symbolTable
from icecream import ic
import sys

def debug_lexer():
    while True:
        text = input("lexer > ")

        result, error = run("<stdin>", text)

        if error:
            print(error.as_string())
        else:
            output_to_symbolTable(result)
            result.pop()
            print(result)

def debug_parser():
    while True:
        text = input("parser > ")

        result, error = run("<stdin>", text)

        if error: print(error.as_string())
        else: print(result)

def debug_interpreter():
    while True:
        text = input("interpreter > ")

        result, error = run("<stdin>", text)

        if error: print(error.as_string())
        else: print(result)


def run(fn, text):
    # Lexer
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    # return tokens, error
    print(tokens)

    # Parser
    if error: return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    # return ast.node, ast.error
    ic(ast.node)

    # Interpreter
    if ast.error: return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result, None

#* Function Calls
# debug_lexer()
# debug_parser()
debug_interpreter()

def run_file(filename):
    if(filename):
        if(filename.lower().endswith('.kkun')):
            try:
                with open(filename, 'r') as f:
                    text = f.read()
                
                result, error = run(filename, text)

                if error:
                    print(error.as_string())
                else:
                    print(format("File name:", ">20") + "      " + filename)
                    print(format('TOKENS', '>20') + '      ' + 'LEXEMES')
                    print('-----------------------------------------------')
                    print(tok_to_str(result))
                    output_to_symbolTable(result)
                    # result.pop()      # diko alam kung mas okay ba to or yung ginayang formatting lang sa symbol table
                    # print(result)
            except FileNotFoundError:
                print("File does not exist!")
        else:
            print("Invalid file name extension!")

OPTIONS = {'-f', '-file', '-c', 'cli'}
lowercasedArgs = [arg.lower() for arg in sys.argv]

if __name__ == '__main__':
    if '-cli' in lowercasedArgs or '-c' in lowercasedArgs:
        while True:
            text = input("cocoon > ")

            result, error = run("<stdin>", text)

            if error:
                print(error.as_string())
            else:
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
import cocoon
import sys

def run(filename):
    if(filename):
        if(filename.lower().endswith('.kkun')):
            try:
                with open(filename, 'r') as f:
                    text = f.read()
                
                result, error = cocoon.run(filename, text)

                if error:
                    print(error.as_string())
                else:
                    print(format("File name:", ">20") + "      " + filename)
                    print(format('TOKENS', '>20') + '      ' + 'LEXEMES')
                    print('-----------------------------------------------')
                    print(cocoon.tok_to_str(result))
                    cocoon.output_to_symbolTable(result)
                    # result.pop()      # diko alam kung mas okay ba to or yung ginayang formatting lang sa symbol table
                    # print(result)
            except FileNotFoundError:
                print("File does not exist!")
        else:
            print("Invalid file name extension!")

OPTIONS = {'-f', '-file', '-c', 'cli'}
lowercasedArgs = [arg.lower() for arg in sys.argv]

if '-cli' in lowercasedArgs or '-c' in lowercasedArgs:
    while True:
        text = input("cocoon > ")

        result, error = cocoon.run("<stdin>", text)

        if error:
            print(error.as_string())
        else:
            cocoon.output_to_symbolTable(result)
            result.pop()
            print(result)
elif '-file' in lowercasedArgs or '-f' in lowercasedArgs:
    if '-f' in lowercasedArgs:
        flagidx = lowercasedArgs.index('-f') 
    elif '-file' in lowercasedArgs:
        flagidx = lowercasedArgs.index('-file')
    try:
        run(sys.argv[flagidx + 1])
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
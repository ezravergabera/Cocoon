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
            

if '-c' in sys.argv:
    while True:
        text = input("cocoon > ")

        result, error = cocoon.run("<stdin>", text)

        if error:
            print(error.as_string())
        else:
            cocoon.output_to_symbolTable(result)
            result.pop()
            print(result)
elif '-f' in sys.argv:
    flagidx = sys.argv.index('-f')
    try:
        run(sys.argv[flagidx + 1])
    except IndexError:
        print("No file name argument is found!")
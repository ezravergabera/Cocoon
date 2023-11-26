import cocoon

while True:
    text = input("cocoon > ")

    result, error = cocoon.run("<stdin>", text)

    if error:
        print(error.as_string())
    else:
        cocoon.output_to_symbolTable(result)
        result.pop()
        print(result)
import cocoon

while True:
    text = input('cocoon > ')

    result, error = cocoon.run(text)

    if error:
        print(error.as_string())
    else:
        print(result)


// enloooooooooooooooo
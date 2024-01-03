def foundChar():
    return True

def notFound():
    return False

alphaDict = {
    "a":foundChar,
    "b":foundChar,
    "c":foundChar,
    "d":foundChar,
    "e":foundChar,
    "f":foundChar,
    "g":foundChar,
    "h":foundChar,
    "i":foundChar,
    "j":foundChar,
    "k":foundChar,
    "l":foundChar,
    "m":foundChar,
    "n":foundChar,
    "o":foundChar,
    "p":foundChar,
    "q":foundChar,
    "r":foundChar,
    "s":foundChar,
    "t":foundChar,
    "u":foundChar,
    "v":foundChar,
    "w":foundChar,
    "x":foundChar,
    "y":foundChar,
    "z":foundChar,
    "A":foundChar,
    "B":foundChar,
    "C":foundChar,
    "D":foundChar,
    "E":foundChar,
    "F":foundChar,
    "G":foundChar,
    "H":foundChar,
    "I":foundChar,
    "J":foundChar,
    "K":foundChar,
    "L":foundChar,
    "M":foundChar,
    "N":foundChar,
    "O":foundChar,
    "P":foundChar,
    "Q":foundChar,
    "R":foundChar,
    "S":foundChar,
    "T":foundChar,
    "U":foundChar,
    "V":foundChar,
    "W":foundChar,
    "X":foundChar,
    "Y":foundChar,
    "Z":foundChar
}

digitsDict = {
    "0":foundChar,
    "1":foundChar,
    "2":foundChar,
    "3":foundChar,
    "4":foundChar,
    "5":foundChar,
    "6":foundChar,
    "7":foundChar,
    "8":foundChar,
    "9":foundChar
}

whitespacesDict = {
    "":foundChar,
    " ":foundChar,
    "\t":foundChar,
    "\n":foundChar,
    "\v":foundChar,
    "\r":foundChar
}

operatorsDict = {
    "+":foundChar,
    "-":foundChar,
    "*":foundChar,
    "/":foundChar,
    "~":foundChar,
    "^":foundChar,
    "%":foundChar,
    "=":foundChar,
    ">":foundChar,
    "<":foundChar,
    "!":foundChar,
    "&":foundChar,
    "|":foundChar
}

punctuationDict = {
    ".":foundChar,
    ",":foundChar,
    ";":foundChar,
    "(":foundChar,
    ")":foundChar,
    "[":foundChar,
    "]":foundChar
}

untrackedDict = {
    "$":foundChar,
    "#":foundChar,
    "@":foundChar,
    "`":foundChar,
    "?":foundChar,
    "}":foundChar,
    "{":foundChar,
    "\\":foundChar,
    ":":foundChar
}

def isAlphabet(char):
    func = alphaDict.get(char, notFound)
    return func()

def isDigits(char):
    func = digitsDict.get(char, notFound)
    return func()

def isWhitespace(char):
    func = whitespacesDict.get(char, notFound)
    return func()

def isOperator(char):
    func = operatorsDict.get(char, notFound)
    return func()

def isPunctuation(char):
    func = punctuationDict.get(char, notFound)
    return func()

def isUntracked(char):
    func = untrackedDict.get(char, notFound)
    return func()

def isinCharSet(char):
    func1 = alphaDict.get(char, notFound)
    func2 = digitsDict.get(char, notFound)
    func3 = whitespacesDict.get(char, notFound)
    func4 = operatorsDict.get(char, notFound)
    func5 = punctuationDict.get(char, notFound)
    
    if func1():
        return func1()
    elif func2():
        return func2()
    elif func3():
        return func3()
    elif func4():
        return func4()
    elif func5():
        return func5()
    else:
        return False
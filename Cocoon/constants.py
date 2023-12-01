ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
WHITESPACES = ' \t\n\v\r'
OPERATORS = '+-/*^%'
UNARY = '+-'
RELATIONAL = '=!><'
LOGICAL = {
    "NOT", 
    "AND", 
    "OR", 
    "not", 
    "and", 
    "or"
}
PUNCTUATIONS = '()[]'
CONSTANTS = {
    "number", 
    "num", 
    "decimal", 
    "deci", 
    "text", 
    "character", 
    "char", 
    "boolean", 
    "bool"
}
KEYWORDS = {
    "show", 
    "get" 
}
NOISEWORDS = {
    "do", 
    "start", 
    "end"
}
RESERVEDWORDS = {
    "true", 
    "false", 
    "done", 
    "next", 
    "give", 
    "group", 
    "build", 
    "ask", 
    "askmore", 
    "more", 
    "repeat", 
    "while", 
    "enough", 
    "empty", 
    "undefined", 
    "undef"
    "exit", 
    "raise", 
    "raising"
}
UNTRACKED = '$#@`~?}{\\:;'
INVALID = {
    "!",
    "&",
    "|",
    "&&",
    "||"
}
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int ln;
    char* fn;
} Position;

typedef struct {
    Position pos_start;
    Position pos_end;
    char* error_name;
    char* details;
} Error;

void init_error(Error* error, Position pos_start, Position pos_end, char* error_name, char* details) {
    error->pos_start = pos_start;
    error->pos_end = pos_end;
    error->error_name = error_name;
    error->details = details;
}

char* error_as_string(Error* error) {
    char* result = malloc(1000 * sizeof(char));
    sprintf(result, "%s: %s", error->error_name, error->details);
    sprintf(result, "%s\nFile %s, line %d", result, error->pos_start.fn, error->pos_start.ln + 1);
    return result;
}

typedef struct {
    Position pos_start;
    Position pos_end;
    char* details;
} IllegalCharError;

void init_illegal_char_error(IllegalCharError* error, Position pos_start, Position pos_end, char* details) {
    init_error((Error*)error, pos_start, pos_end, "Illegal Character", details);
}

typedef struct {
    Position pos_start;
    Position pos_end;
    char* details;
} IllegalIdentifierError;

void init_illegal_identifier_error(IllegalIdentifierError* error, Position pos_start, Position pos_end, char* details) {
    init_error((Error*)error, pos_start, pos_end, "Illegal Identifier", details);
}

typedef struct {
    Position pos_start;
    Position pos_end;
    char* details;
} IllegalNumberError;

void init_illegal_number_error(IllegalNumberError* error, Position pos_start, Position pos_end, char* details) {
    init_error((Error*)error, pos_start, pos_end, "Illegal Number", details);
}

typedef struct {
    Position pos_start;
    Position pos_end;
    char* details;
} LexicalError;

void init_lexical_error(LexicalError* error, Position pos_start, Position pos_end, char* details) {
    init_error((Error*)error, pos_start, pos_end, "Lexical Error", details);
}

typedef struct {
    Position pos_start;
    Position pos_end;
    char* details;
} InvalidDecimalError;

void init_invalid_decimal_error(InvalidDecimalError* error, Position pos_start, Position pos_end, char* details) {
    init_error((Error*)error, pos_start, pos_end, "Invalid Decimal", details);
}

typedef struct {
    Position pos_start;
    Position pos_end;
    char* details;
} InvalidRelationalSymbol;

void init_invalid_relational_symbol(InvalidRelationalSymbol* error, Position pos_start, Position pos_end, char* details) {
    init_error((Error*)error, pos_start, pos_end, "Invalid Symbol", details);
}

typedef struct {
    Position pos_start;
    Position pos_end;
    char* details;
} ReferenceError;

void init_reference_error(ReferenceError* error, Position pos_start, Position pos_end, char* details) {
    init_error((Error*)error, pos_start, pos_end, "Reference Error", details);
}



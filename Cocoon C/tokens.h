#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char* type;
    char* value;
} Token;

Token* createToken(char* type, char* value) {
    Token* token = (Token*)malloc(sizeof(Token));
    token->type = type;
    token->value = value;
    return token;
}

void printToken(Token* token) {
    if (token->value != NULL) {
        printf("%-20s    %s\n", token->type, token->value);
    } else {
        printf("%-20s    %s\n", token->type, token->type);
    }
}

void printTokens(char* fn, Token** tokens) {
    printf("%-20s    %s\n", "File name:", fn);
    printf("%-20s    %s\n", "TOKENS", "LEXEMES");
    printf("----------------------------------------\n");
    for (int i = 0; tokens[i] != NULL; i++) {
        printToken(tokens[i]);
    }
}

void outputToSymbolTable(Token** tokens) {
    char* filename = "symbolTable.txt";
    FILE* f = fopen(filename, "w");
    if (f == NULL) {
        printf("Error opening file.\n");
        return;
    }
    fprintf(f, "%-20s    %s\n", "File name:", filename);
    fprintf(f, "%-20s    %s\n", "TOKENS", "LEXEMES");
    fprintf(f, "----------------------------------------\n");
    for (int i = 0; tokens[i] != NULL; i++) {
        printToken(tokens[i]);
    }
    fclose(f);
}



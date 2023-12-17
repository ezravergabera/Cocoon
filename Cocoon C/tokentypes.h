#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 100

typedef struct {
    char type[MAX_LEN];
    char value[MAX_LEN];
} token;

int main() {
    char TT_ID[] = "Identifier";
    char TT_ASSIGN[] = "Assignment";
    char TT_PLUS[] = "PLUS";
    char TT_MINUS[] = "MINUS";
    char TT_MUL[] = "MUL";
    char TT_DIV[] = "DIV";
    char TT_INTDIV[] = "INTDIV";
    char TT_EXPO[] = "EXPO";
    char TT_MOD[] = "MOD";
    char TT_INCRE[] = "INCREMENT";
    char TT_DECRE[] = "DECREMENT";
    char TT_POSITIVE[] = "POSITIVE";
    char TT_NEGATIVE[] = "NEGATIVE";
    char TT_GREATER[] = "Greater_than";
    char TT_LESS[] = "Less_than";
    char TT_GREATEREQUAL[] = "Greater_Equal";
    char TT_LESSEQUAL[] = "Less_Equal";
    char TT_EQUALTO[] = "Equal_to";
    char TT_NOTEQUAL[] = "Not_Equal";
    char TT_NOT[] = "NOT";
    char TT_AND[] = "AND";
    char TT_OR[] = "OR";
    char TT_INT[] = "Number";
    char TT_FLOAT[] = "Decimal";
    char TT_STR[] = "Text";
    char TT_BOOL[] = "Bool";
    char TT_DTYPE[] = "Data_Type";
    char TT_KWORD[] = "Keyword";
    char TT_RWORD[] = "Reserved_Word";
    char TT_NWORD[] = "Noise_Word";
    char TT_COMMENT[] = "Comment";
    char TT_DOT[] = "Dot";
    char TT_COMMA[] = "Comma";
    char TT_SEMICOLON[] = "Semicolon";
    char TT_LSQUARE[] = "Left_Square";
    char TT_RSQUARE[] = "Right_Square";
    char TT_LPAREN[] = "Left_Paren";
    char TT_RPAREN[] = "Right_Paren";
    char TT_EOF[] = "EOF";

    return 0;
}



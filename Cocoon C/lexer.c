#include "check.h"
#include "errors.h"
#include "position.h"
#include "tokens.h"
#include "tokentypes.h"

typedef struct
{
    char *fn;
    char *text;
    Position pos;
    char current_char;
} Lexer;

Lexer *init_lexer(char *fn, char *text)
{
    Lexer *lexer = (Lexer *)malloc(sizeof(Lexer));
    lexer->fn = fn;
    lexer->text = text;
    lexer->pos = init_position(-1, 0, -1, fn, text);
    lexer->current_char = '\0';
    advance(lexer);
    return lexer;
}

void advance(Lexer *lexer)
{
    advance_position(&(lexer->pos), lexer->current_char);
    lexer->current_char = lexer->text[lexer->pos.idx] != '\0' ? lexer->text[lexer->pos.idx] : '\0';
}

char check(Lexer *lexer)
{
    char next_char = lexer->text[lexer->pos.idx + 1] != '\0' ? lexer->text[lexer->pos.idx + 1] : '\0';
    return next_char != '\0' ? next_char : '\0';
}

char backtrack(Lexer *lexer)
{
    char prev_char = lexer->text[lexer->pos.idx - 1] != '\0' ? lexer->text[lexer->pos.idx - 1] : '\0';
    return prev_char != '\0' ? prev_char : '\0';
}

Token *make_tokens(Lexer *lexer)
{
    Token **tokens = (Token **)malloc(sizeof(Token *));
    int tokens_size = 0;
    while (lexer->current_char != '\0')
    {
        char next_char = lexer->current_char;
        char check = check(lexer);

        if (isWhitespace(char))
        {
            advance(lexer);
        }

        else if (isAlphabet(char) || char == '_')
        {
            void *result = make_identifier(lexer);
            if (result != NULL)
            {
                if (strcmp(result, "Token") == 0)
                {
                    tokens[tokens_size++] = (Token *)result;
                }
                else if (strcmp(result, "Error") == 0)
                {
                    return NULL;
                }
            }
        }

        else if (isOperator(char))
        {
            void *result = make_operator(lexer);
            if (result != NULL)
            {
                if (strcmp(result, "Token") == 0)
                {
                    tokens[tokens_size++] = (Token *)result;
                }
                else if (strcmp(result, "Error") == 0)
                {
                    return NULL;
                }
            }
        }

        else if (char == '.' && check == '.' && !isWhitespace(check))
        {
            void *result = make_comments(lexer);
            if (result != NULL)
            {
                if (strcmp(result, "Token") == 0)
                {
                    tokens[tokens_size++] = (Token *)result;
                }
                else if (strcmp(result, "Error") == 0)
                {
                    return NULL;
                }
            }
        }

        else if (isDigits(char) || char == '.')
        {
            void *result = make_number(lexer);
            if (result != NULL)
            {
                if (strcmp(result, "Token") == 0)
                {
                    tokens[tokens_size++] = (Token *)result;
                }
                else if (strcmp(result, "Error") == 0)
                {
                    return NULL;
                }
            }
        }

        else if ((isInvalid(char) && isWhitespace(check)) || (isInvalid(char) && char == check))
        {
            return NULL;
        }

        else if (isRelational(char))
        {
            void *result = make_relational(lexer);
            if (result != NULL)
            {
                if (strcmp(result, "Token") == 0)
                {
                    tokens[tokens_size++] = (Token *)result;
                }
                else if (strcmp(result, "Error") == 0)
                {
                    return NULL;
                }
            }
        }

        else if (char == '"' || char == "'")
        {
            void *result = make_string(lexer);
            if (result != NULL)
            {
                if (strcmp(result, "Token") == 0)
                {
                    tokens[tokens_size++] = (Token *)result;
                }
                else if (strcmp(result, "Error") == 0)
                {
                    return NULL;
                }
            }
        }

        else if (isPunctuation(char))
        {
            tokens[tokens_size++] = make_punctuation(lexer);
            advance(lexer);
        }

        else
        {
            Position *pos_start = copy_position(&(lexer->pos));
            char char = lexer->current_char;
            advance(lexer);
            return NULL;
        }
    }

    tokens[tokens_size++] = init_token("TT_EOF", TT_EOF);
    return tokens;
}

void *make_identifier(Lexer *lexer)
{
    char *lexeme = "";
    TokenType tokentype = TT_ID;
    Position *pos_start = copy_position(&(lexer->pos));
    while (lexer->current_char != '\0' && (isAlphabet(lexer->current_char) || isDigits(lexer->current_char) || isWhitespace(lexer->current_char) || isUntracked(lexer->current_char) || lexer->current_char == '_'))
    {

        if (isWhitespace(lexer->current_char))
        {
            break;
        }

        else if (lexer->current_char == 'A' && strlen(lexeme) == 0)
        {
            lexeme += lexer->current_char;
            advance(lexer);
            if (lexer->current_char == 'N')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'D')
                {
                    lexeme += lexer->current_char;
                    tokentype = TT_AND;
                    advance(lexer);
                }
            }
        }

        else if (lexer->current_char == 'a' && strlen(lexeme) == 0)
        {
            lexeme += lexer->current_char;
            advance(lexer);
            if (lexer->current_char == 'n')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'd')
                {
                    lexeme += lexer->current_char;
                    tokentype = TT_AND;
                    advance(lexer);
                }

                else if (lexer->current_char == 's')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 'k')
                    {
                        lexeme += lexer->current_char;
                        tokentype = TT_RWORD;
                        advance(lexer);
                        if (lexer->current_char == 'm')
                        {
                            lexeme += lexer->current_char;
                            tokentype = TT_ID;
                            advance(lexer);
                            if (lexer->current_char == 'o')
                            {
                                lexeme += lexer->current_char;
                                advance(lexer);
                                if (lexer->current_char == 'r')
                                {
                                    lexeme += lexer->current_char;
                                    advance(lexer);
                                    if (lexer->current_char == 'e')
                                    {
                                        lexeme += lexer->current_char;
                                        tokentype = TT_RWORD;
                                        advance(lexer);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        else if (lexer->current_char == 'b' && strlen(lexeme) == 0)
        {
            lexeme += lexer->current_char;
            advance(lexer);

            if (lexer->current_char == 'o')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'o')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 'l')
                    {
                        lexeme += lexer->current_char;
                        tokentype = TT_DTYPE;

                        advance(lexer);
                        if (lexer->current_char == 'e')
                        {
                            lexeme += lexer->current_char;
                            tokentype = TT_ID;
                            advance(lexer);
                            if (lexer->current_char == 'a')
                            {
                                lexeme += lexer->current_char;
                                advance(lexer);
                                if (lexer->current_char == 'n')
                                {
                                    lexeme += lexer->current_char;
                                    tokentype = TT_DTYPE;
                                    advance(lexer);
                                }
                            }
                        }
                    }
                }
            }

            else if (lexer->current_char == 'u')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'i')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 'l')
                    {
                        lexeme += lexer->current_char;
                        advance(lexer);
                        if (lexer->current_char == 'd')
                        {
                            lexeme += lexer->current_char;
                            tokentype = TT_RWORD;
                            advance(lexer);
                        }
                    }
                }
            }
        }

        else if (lexer->current_char == 'c' && strlen(lexeme) == 0)
        {
            lexeme += lexer->current_char;
            advance(lexer);
            if (lexer->current_char == 'h')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'a')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 'r')
                    {
                        lexeme += lexer->current_char;
                        tokentype = TT_DTYPE;
                        advance(lexer);
                        if (lexer->current_char == 'a')
                        {
                            lexeme += lexer->current_char;
                            tokentype = TT_ID;
                            advance(lexer);
                            if (lexer->current_char == 'c')
                            {
                                lexeme += lexer->current_char;
                                advance(lexer);
                                if (lexer->current_char == 't')
                                {
                                    lexeme += lexer->current_char;
                                    advance(lexer);
                                    if (lexer->current_char == 'e')
                                    {
                                        lexeme += lexer->current_char;
                                        advance(lexer);
                                        if (lexer->current_char == 'r')
                                        {
                                            lexeme += lexer->current_char;
                                            tokentype = TT_DTYPE;
                                            advance(lexer);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        else if (lexer->current_char == 'd' && strlen(lexeme) == 0)
        {

            lexeme += lexer->current_char;
            advance(lexer);
            if (lexer->current_char == 'o')
            {
                lexeme += lexer->current_char;
                tokentype = TT_NWORD;
                advance(lexer);

                if (lexer->current_char == 'n')
                {
                    lexeme += lexer->current_char;
                    tokentype = TT_ID;
                    advance(lexer);
                    if (lexer->current_char == 'e')
                    {
                        lexeme += lexer->current_char;
                        tokentype = TT_RWORD;
                        advance(lexer);
                    }
                }
            }

            else if (lexer->current_char == 'e')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'c')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 'i')
                    {
                        lexeme += lexer->current_char;
                        tokentype = TT_DTYPE;
                        advance(lexer);

                        if (lexer->current_char == 'm')
                        {
                            lexeme += lexer->current_char;
                            tokentype = TT_ID;
                            advance(lexer);
                            if (lexer->current_char == 'a')
                            {
                                lexeme += lexer->current_char;
                                advance(lexer);
                                if (lexer->current_char == 'l')
                                {
                                    lexeme += lexer->current_char;
                                    tokentype = TT_DTYPE;
                                    advance(lexer);
                                }
                            }
                        }
                    }
                }
            }
        }

        else if (lexer->current_char == 'e' && strlen(lexeme) == 0)
        {
            lexeme += lexer->current_char;
            advance(lexer);

            if (lexer->current_char == 'm')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'p')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 't')
                    {
                        lexeme += lexer->current_char;
                        advance(lexer);
                        if (lexer->current_char == 'y')
                        {
                            lexeme += lexer->current_char;
                            tokentype = TT_RWORD;
                            advance(lexer);
                        }
                    }
                }
            }

            else if (lexer->current_char == 'x')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'i')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 't')
                    {
                        lexeme += lexer->current_char;
                        tokentype = TT_RWORD;
                        advance(lexer);
                        if ((isWhitespace(check(lexer)) || check(lexer) == '\0') && lexer->fn != "<stdin>")
                        {
                            return init_reference_error(pos_start, &(lexer->pos), "Usage of a reserved word.");
                        }
                        else if (isWhitespace(check(lexer)) || check(lexer) == '\0')
                        {
                            exit(0);
                        }
                    }
                }
            }

            else if (lexer->current_char == 'n')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'd')
                {
                    lexeme += lexer->current_char;
                    tokentype = TT_NWORD;
                    advance(lexer);

                    if (lexer->current_char == 'o')
                    {
                        lexeme += lexer->current_char;
                        advance(lexer);
                        if (lexer->current_char == 'u')
                        {
                            lexeme += lexer->current_char;
                            advance(lexer);
                            if (lexer->current_char == 'g')
                            {
                                lexeme += lexer->current_char;
                                advance(lexer);
                                if (lexer->current_char == 'h')
                                {
                                    lexeme += lexer->current_char;
                                    tokentype = TT_RWORD;
                                    advance(lexer);
                                }
                            }
                        }
                    }
                }
            }
        }

        else if (lexer->current_char == 'f' && strlen(lexeme) == 0)
        {
            lexeme += lexer->current_char;
            advance(lexer);
            if (lexer->current_char == 'a')
            {
                lexeme += lexer->current_char;
                advance(lexer);
                if (lexer->current_char == 'l')
                {
                    lexeme += lexer->current_char;
                    advance(lexer);
                    if (lexer->current_char == 's')
                    {
                        lexeme += lexer->current_char;
                        advance(lexer);
                        if (lexer->current_char == 'e')
                        {
                            lexeme += lexer->current_char;
                            tokentype = TT_BOOL;
                            advance(lexer);
                        }
                    }
                }
            }
        }
    }

    return init_token(lexeme, tokentype);
}

Token make_comments(Lexer *self)
{
    Position pos_start = copy_position(self->pos);
    char *comment_str = malloc(sizeof(char));
    comment_str[0] = '\0';
    char current_char = self->current_char;
    advance(self);
    char check = check(self);
    int dot_count = 0;
    if (current_char == '.' && check == '.' && !isWhitespace(check))
    {
        while (dot_count != 3)
        {
            comment_str = realloc(comment_str, (strlen(comment_str) + 2) * sizeof(char));
            strcat(comment_str, &current_char);
            if (check == '\0' && check != NULL)
            {
                return create_lexical_error(pos_start, self->pos, "Closing symbol not found.");
            }
            if (current_char == '.')
            {
                dot_count += 1;
            }
            else
            {
                dot_count = 0;
            }
            advance(self);
        }
    }
    else
    {
        comment_str = realloc(comment_str, (strlen(comment_str) + 2) * sizeof(char));
        strcat(comment_str, &current_char);
        advance(self);
        while (current_char != '\n' && current_char != '\0')
        {
            comment_str = realloc(comment_str, (strlen(comment_str) + 2) * sizeof(char));
            strcat(comment_str, &current_char);
            advance(self);
        }
    }
    if (current_char == '\n')
    {
        advance(self);
    }
    return create_token(TT_COMMENT, comment_str);
}

Token make_operator(Lexer *self)
{
    char operator= self->current_char;
    advance(self);
    if (operator== '+')
    {
        return create_token(TT_PLUS, &operator);
    }
    else if (operator== '-')
    {
        return create_token(TT_MINUS, &operator);
    }
    else if (operator== '*')
    {
        return create_token(TT_MUL, &operator);
    }
    else if (operator== '/')
    {
        return create_token(TT_DIV, &operator);
    }
    else if (operator== '~')
    {
        return create_token(TT_INTDIV, &operator);
    }
    else if (operator== '^')
    {
        return create_token(TT_EXPO, &operator);
    }
    else if (operator== '%')
    {
        return create_token(TT_MOD, &operator);
    }
}

Token make_number(Lexer *self)
{
    char *num_str = malloc(sizeof(char));
    num_str[0] = '\0';
    int dot_count = 0;
    bool isValid = true;
    bool isIdentifier = false;
    Position pos_start = copy_position(self->pos);
    while (self->current_char != '\0' && (isAlphabet(self->current_char) || isDigits(self->current_char) || isWhitespace(self->current_char) || isUntracked(self->current_char) || self->current_char == '_' || self->current_char == '.'))
    {
        char check = check(self);
        if (isWhitespace(self->current_char))
        {
            break;
        }
        else if (num_str && self->current_char == '_' && check == '_' || isValid == false)
        {
            isValid = false;
            num_str = realloc(num_str, (strlen(num_str) + 2) * sizeof(char));
            strcat(num_str, &self->current_char);
        }
        else if (isAlphabet(self->current_char) || isUntracked(self->current_char))
        {
            isValid = false;
            num_str = realloc(num_str, (strlen(num_str) + 2) * sizeof(char));
            strcat(num_str, &self->current_char);
        }
        else if ((not num_str && isDigits(self->current_char)) && isAlphabet(check) && not isWhitespace(check))
        {
            isIdentifier = true;
            num_str = realloc(num_str, (strlen(num_str) + 2) * sizeof(char));
            strcat(num_str, &self->current_char);
        }
        else if (self->current_char == '.')
        {
            if (dot_count == 1)
            {
                dot_count += 1;
            }
            dot_count += 1;
            num_str = realloc(num_str, (strlen(num_str) + 2) * sizeof(char));
            strcat(num_str, ".");
        }
        else
        {
            if (self->current_char != '_')
            {
                num_str = realloc(num_str, (strlen(num_str) + 2) * sizeof(char));
                strcat(num_str, &self->current_char);
            }
        }
        advance(self);
    }
    if (dot_count == 0 && isValid == true && isIdentifier == false)
    {
        int num = atoi(num_str);
        free(num_str);
        return create_token(TT_INT, &num);
    }
    else if (dot_count == 2 && isValid == true)
    {
        return create_lexical_error(pos_start, self->pos, num_str);
    }
    else if (isIdentifier)
    {
        return create_illegal_identifier_error(pos_start, self->pos, num_str);
    }
    else if (isValid == false)
    {
        return create_illegal_number_error(pos_start, self->pos, num_str);
    }
    else if (strcmp(num_str, ".") == 0)
    {
        free(num_str);
        return create_token(TT_DOT, num_str);
    }
    else
    {
        double num = atof(num_str);
        free(num_str);
        return create_token(TT_FLOAT, &num);
    }
}

Token invalid_relational(Lexer *self)
{
    char *rel_str = malloc(sizeof(char));
    rel_str[0] = '\0';
    while (self->current_char != '\0' && isInvalid(self->current_char))
    {
        char check = check(self);
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        Position pos_start = copy_position(self->pos);
        if (strcmp(rel_str, "!") == 0 && isWhitespace(check))
        {
            advance(self);
            return create_invalid_relational_symbol(pos_start, self->pos, rel_str, "Consider using \"not\" or \"NOT\" instead.");
        }
        else if (strcmp(rel_str, "&") == 0 && isWhitespace(check))
        {
            advance(self);
            return create_invalid_relational_symbol(pos_start, self->pos, rel_str, "Consider using \"and\" or \"AND\" instead.");
        }
        else if (strcmp(rel_str, "|") == 0 && isWhitespace(check))
        {
            advance(self);
            return create_invalid_relational_symbol(pos_start, self->pos, rel_str, "Consider using \"or\" or \"OR\" instead.");
        }
        else if (strcmp(rel_str, "&") == 0 && check == '&')
        {
            advance(self);
            rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
            strcat(rel_str, &self->current_char);
            advance(self);
            return create_invalid_relational_symbol(pos_start, self->pos, rel_str, "Consider using \"and\" or \"AND\" instead.");
        }
        else if (strcmp(rel_str, "|") == 0 && check == '|')
        {
            advance(self);
            rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
            strcat(rel_str, &self->current_char);
            advance(self);
            return create_invalid_relational_symbol(pos_start, self->pos, rel_str, "Consider using \"or\" or \"OR\" instead.");
        }
        else
        {
            advance(self);
            return create_illegal_char_error(pos_start, self->pos, self->current_char);
        }
    }
}

Token make_relational(Lexer *self)
{
    char *rel_str = malloc(sizeof(char));
    rel_str[0] = '\0';
    char check = check(self);
    if (self->current_char == '=' && check != '=')
    {
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        return create_token(TT_ASSIGN, rel_str);
    }
    else if (self->current_char == '>' && check == '=')
    {
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        return create_token(TT_GREATEREQUAL, rel_str);
    }
    else if (self->current_char == '<' && check == '=')
    {
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        return create_token(TT_LESSEQUAL, rel_str);
    }
    else if (self->current_char == '=' && check == '=')
    {
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        return create_token(TT_EQUALTO, rel_str);
    }
    else if (self->current_char == '!' && check == '=')
    {
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        return create_token(TT_NOTEQUAL, rel_str);
    }
    else if (self->current_char == '>')
    {
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        return create_token(TT_GREATER, rel_str);
    }
    else if (self->current_char == '<')
    {
        rel_str = realloc(rel_str, (strlen(rel_str) + 2) * sizeof(char));
        strcat(rel_str, &self->current_char);
        advance(self);
        return create_token(TT_LESS, rel_str);
    }
}

Token make_string(Lexer *self)
{
    char *text_str = malloc(sizeof(char));
    text_str[0] = '\0';
    char stop = self->current_char;
    text_str = realloc(text_str, (strlen(text_str) + 2) * sizeof(char));
    strcat(text_str, &stop);
    Position pos_start = copy_position(self->pos);
    advance(self);
    while (self->current_char != '\0' && self->current_char != stop)
    {
        text_str = realloc(text_str, (strlen(text_str) + 2) * sizeof(char));
        strcat(text_str, &self->current_char);
        advance(self);
    }
    if (self->current_char == stop)
    {
        text_str = realloc(text_str, (strlen(text_str) + 2) * sizeof(char));
        strcat(text_str, &stop);
        advance(self);
    }
    else
    {
        return create_lexical_error(pos_start, self->pos, "Must be enclosed by \" or \'.");
    }
    return create_token(TT_STR, text_str);
}

Token make_punctuation(Lexer *self)
{
    if (isPunctuation(self->current_char))
    {
        char *char = malloc(sizeof(char));
        *char = self->current_char;
        advance(self);
        if (*char == '.')
        {
            return create_token(TT_DOT, char);
        }
        if (*char == ',')
        {
            return create_token(TT_COMMA, char);
        }
        else if (*char == ';')
        {
            return create_token(TT_SEMICOLON, char);
        }
        else if (*char == '[')
        {
            return create_token(TT_LSQUARE, char);
        }
        else if (*char == ']')
        {
            return create_token(TT_RSQUARE, char);
        }
        else if (*char == '(')
        {
            return create_token(TT_LPAREN, char);
        }
        else if (*char == ')')
        {
            return create_token(TT_RPAREN, char);
        }
    }
}
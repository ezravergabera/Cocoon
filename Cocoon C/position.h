#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define Position struct with typedef
typedef struct {
    int idx;
    int ln;
    int col;
    const char* fn;
    const char* ftext;
} Position;

Position* create_position(int idx, int ln, int col, const char* fn, const char* ftext) {
    Position* position = (Position*)malloc(sizeof(Position));
    position->idx = idx;
    position->ln = ln;
    position->col = col;
    position->fn = strdup(fn);
    position->ftext = strdup(ftext);
    return position;
}

// Implementation of advance function
void advance(Position* position, char current_char) {
    position->idx += 1;
    position->col += 1;
    if (current_char == '\n') {
        position->ln += 1;
        position->col = 0;
    }
}

// Implementation of copy function
Position* copy(Position* position) {
    return create_position(position->idx, position->ln, position->col, position->fn, position->ftext);
}

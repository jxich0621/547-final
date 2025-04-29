#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>

int main() {
    char input[128];
    fgets(input, sizeof(input), stdin);

    int a = strlen(input) % 7;
    int b = 0;
    int c = 4;
    int* d = NULL;

    if(a % 6 == 0) {
        c = a/b;
    } else if(a % 6 == 1) {
        c = *d;
    } else if(a % 6 == 2) {
        assert(c == 3);
    } else{
        c = 5;
    }
    
    return 0;
    
}

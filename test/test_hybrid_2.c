#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>

int main() {
    char input[128];
    fgets(input, sizeof(input), stdin);

    int a = strlen(input) % 7;
    int b = 1;
    int c = 4;
    int* d = NULL;

    int e = 9;
    int f = a + 9;
    int g = f*e;
    int h = a*e % 318;

    if(a % 6 == 0) {
        if (h % 4 == 1){
            b = 0;
        }
        c = a/b;
    } else if(a % 6 == 1) {
        if (h % 3 == 1){
            d = &a;
        }
        c = *d;
    } else if(a % 6 == 2) {
        if (h % 7 == 1){
            c = 3;
        }
        assert(c == 3);
    } else{
        c = 5;
    }
    
    return 0;
    
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int main() {

    int a = getchar() % 7 + 1;
    int b = getchar()  % 13 + 1;

    int *c = NULL;

    int d = 4;

    while(a < b){
        d = a + b - *c;
        a = b + 1;
    }
    c = malloc(sizeof(int) * 10);

    return 0;
}

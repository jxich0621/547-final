#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char input[128];
    fgets(input, sizeof(input), stdin);

    int a = strlen(input) % 7 + 1;
    int b = strlen(input) % 13 + 2;

    int c = a >> b;
    int d = a + b - c;
    int e = a - b + c;
    int f = a / (b*b + 1);
    int g = a % (b*c*b*c + 1);
    int h = a & b & c & d & e & f & g + 1001;

    g = g / (h+8);
    g = g << 1;
    g = g + 100;

    if (f > 0) {
        f = f / 2;
        if ((e & f & g) % 2) {
            g *= (g + c);
        } else if (b < 6) {
            h = e*5 - 1;
        }
        if ((h + 0) - 3 == 0) {
            g = g * (e+7);
        }
    }
  
    if (a % 2 == 0) {
        h = d+e-2*a + 8;
    }

    if (b % 2 == 1){
        g = -8;
    }

    if (c % 3 == 1){
        h = 1;
    }

    c = c/(h+g);

    return 0;
}

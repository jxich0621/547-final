#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char input[128];
    fgets(input, sizeof(input), stdin);

    int a = strlen(input) % 7 + 1;
    int b = strlen(input) % 13 + 2;

    int c = a >> b + 3;
    int d = a + b - c;
    int e = a - b + c;
    int f = a / (b*b + 1);
    int g = a % (b*c*b*c + 1);
    int h = a & b & c & d & e & f & g + 1001;
    int i = 8 + e << 5;
    int j = 8 + f << 10;
    int k = (a * b * c * d * e * f * g * h + 1001) % 233;
    int l = (a + b + c * d - e << 3) % 129;

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

    if (l > 0) {
        g = g / (h + 8);
        g = g << 1;
        g = g + 100;
        switch (k) {
            case 0:
                i = i / (c + 8);
                break;
            case 1:
                d = d + 100;
                break;
            case 2:
                e = (e - 100) / 66;
                break;
            default:
                break;
        }
    }

    while(b < 15){
        b = b + 1;
        if (b % 2 == 0) {
            //some crazy code, no division operation
            i = i * 3 + 1;
            j = j * 2 + 2;
            k = k * 4 + 3;
        } else {
            h = h*100/ (c*c + 8);
        }
    }
  
    if (a % 2 == 0) {
        h = d+e-2*a + 8;
    }

    if (b % 2 == 1){
        g = -8;
    }

    if (c % 3 == 1){
        h = -8;
    }

    if (d % 4 == 0){
        g = 8;
    }

    c = c/(h+g);

    return 0;
}

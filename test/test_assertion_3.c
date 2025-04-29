#include <stdio.h>
#include <assert.h>

int find_max(int arr[], int size) {
    if (size == 0) {
        return -2147483648; 
    }

    int max_value = arr[0];  

    for (int i = 1; i < size; i++) {
        if (arr[i] > max_value) {
            max_value = arr[i];
        }
    }

    return max_value;
}

int main() {

    int a = getchar() % 7 + 1;
    int b = getchar() % 13 + 3;
    int c = a+b;
    int d = c + 4;

    if(c > 3){
        d += 8;
    }
    if(d > 3){
        c += 8;
    }
    if(b > 4){
        a += 8;
    }
    int arr[] = {3, 7, 2, 9, 5, 8, a};
    int size = sizeof(arr) / sizeof(arr[0]);
    int max_value = find_max(arr, size);

    assert(max_value == 9);
}
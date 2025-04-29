#include <stdio.h>
#include <assert.h>

int count_unique(int arr[], int size) {
    int count = 0;

    for (int i = 0; i < size; i++) {
        int unique = 1;
        for (int j = i + 1; j < size; j++) { 
            if (arr[i] == arr[j]) {
                unique = 0;
                break;
            }
        }
        if (unique) {
            count++;
        }
    }

    return count;
}

int main() {
    int arr[] = {1, 2, 3, 4, 5, 6, 7};

    int a = getchar() % 7 + 3;

    int unique_count;
    
    if(a > 1){
        arr[0] = 8;
    }

    if(a > 3){
        arr[2] = 2;
    }

    unique_count = count_unique(arr, 7);

    assert(unique_count == 7);

    return 0;
}
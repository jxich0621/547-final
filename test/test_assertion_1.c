#include <stdio.h>
#include <assert.h>

int wrong_binary_search(int arr[], int size, int target) {
    int low = 0;
    int high = size;  

    while (low <= high) {
        int mid = (low + high) / 2;

        if (arr[mid] == target)
            return mid;
        else if (arr[mid] < target)
            low = mid + 1;
        else
            high = mid - 1;
    }

    return low; // should return -1 if not found
}

int correct_binary_search(int arr[], int size, int target) {
    int low = 0;
    int high = size - 1;  

    while (low <= high) {
        int mid = (low + high) / 2;

        if (arr[mid] == target)
            return mid;
        else if (arr[mid] < target)
            low = mid + 1;
        else
            high = mid - 1;
    }

    return -1; // should return -1 if not found
}

int main() {
    
    char input[128];
    fgets(input, sizeof(input), stdin);

    int a = strlen(input) % 7 + 1;
    int b = a + 2;
    int c = b + 3;
    int d = c + 4;

    int arr[] = {1, 2, 3, 7, 9, 11, 14};

    printf("Insert: %d, %d, %d, %d\n", a, b, c, d);
    
    int index = wrong_binary_search(arr,7,a);
    int correct_index = correct_binary_search(arr,7,a);
    
    assert(index == correct_index); 

    return 0;
}
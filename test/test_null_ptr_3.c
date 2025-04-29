#include <stdio.h>
#include <stdlib.h>

#define TABLE_SIZE 10

struct Node {
    int key;
    int value;
    struct Node* next;
};

struct HashTable {
    struct Node* buckets[TABLE_SIZE];
};

struct HashTable* createTable() {
    struct HashTable* table = (struct HashTable*)malloc(sizeof(struct HashTable));
    if (table == NULL) return NULL;

    for (int i = 0; i < TABLE_SIZE; i++) {
        table->buckets[i] = NULL;
    }
    return table;
}

int hash(int key) {
    return key % TABLE_SIZE;
}

void insert(struct HashTable* table, int key, int value) {
    int index = hash(key);
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (newNode == NULL) return;
    newNode->key = key;
    newNode->value = value;
    newNode->next = table->buckets[index];
    table->buckets[index] = newNode;
}

int search(struct HashTable* table, int key) {
    int index = hash(key);
    struct Node* node = table->buckets[index];
    
    if (node != NULL){
        if (node->key == key)
            return node->value;
    }

    while (node != NULL) {  

        node = node->next;
        if (node->key == key)
            return node->value;

    }

    return -1; 
}


int main() {
    struct HashTable* table = createTable();

    char input[128];
    fgets(input, sizeof(input), stdin);

    int a = strlen(input) % 3 + 1;
    int b = 1;
    int c = a + 9;

    printf("Insert: %d, %d, %d\n", a, b, c);

    insert(table, a, 100);
    insert(table, b, 200);
    insert(table, c, 300);

    int valueA = search(table, 11);
    
    free(table);  

    return 0;
}
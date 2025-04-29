#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* createNode(int data) {
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    if (node == NULL) return NULL;
    node->data = data;
    node->next = NULL;
    return node;
}

void append(struct Node** head, int data) {
    struct Node* newNode = createNode(data);
    if (*head == NULL) {
        *head = newNode;
        return;
    }
    struct Node* temp = *head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newNode;
}

void processList(struct Node* head) {
    struct Node* cursor = head;
    while (cursor != NULL) {  
        cursor = cursor->next;
        cursor->data += 1;
    }
}

int main() {
    struct Node* head = NULL;

    char input[128];
    fgets(input, sizeof(input), stdin);

    int a = strlen(input) % 7 + 1;
    if(a > 6){a = a + 10;}

    int b = a + 2;
    int c = b + 2;

    if(b > 2){b = b + 10;}
    if(c > 3){c = c + 10;}

    append(&head, a);
    append(&head, b);
    append(&head, c);

    if(a>3){
        processList(head);
    }

    return 0;
}
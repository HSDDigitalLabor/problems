#include <stdio.h>
#include <stdlib.h>

#ifndef LINKED_LIST_TYPES_DEFINED
#define LINKED_LIST_TYPES_DEFINED

typedef struct Node {
  int value;
  struct Node *next;
} Node;

typedef struct List {
  Node *head;
} List;

List *createList(void);
Node *create(int value);
List *insert(List *list, int value);
Node *search(List *list, int value);
int removeNode(List *list, Node *element);
int length(List *list);
Node *get(List *list, int index);
void destroy(List *list);

#endif

// Create an empty list
List *createList(void) {}

// Allocate a new node with the given value
Node *create(int value) {}

// Insert a value at the end of the list
List *insert(List *list, int value) {}

// Search for a value
Node *search(List *list, int value) {}

// Remove a node and return its value
int removeNode(List *list, Node *element) {}

// Return the number of nodes
int length(List *list) {}

// Get node at a specific index
Node *get(List *list, int index) {}

// Free all nodes and the list itself
void destroy(List *list) {}

int main(void) {}

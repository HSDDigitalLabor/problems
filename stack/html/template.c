#include <stdio.h>
#include <stdlib.h>

#ifndef STACK_TYPES_DEFINED
#define STACK_TYPES_DEFINED

typedef struct Node {
  int value;
  struct Node *next;
} Node;

typedef struct Stack {
  Node *top;
} Stack;

Stack *createStack(void);
Node *create(int value);
Stack *push(Stack *stack, int value);
int pop(Stack *stack);
int peek(Stack *stack);
int length(Stack *stack);
void destroy(Stack *stack);

#endif

Stack *createStack(void) {}

Node *create(int value) {}

Stack *push(Stack *stack, int value) {}

int pop(Stack *stack) {}

int peek(Stack *stack) {}

int length(Stack *stack) {}

void destroy(Stack *stack) {}

int main(void) {}
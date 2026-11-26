
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

enum TestResult { TEST_PASS = 0, TEST_FAIL = 1 };

int main(int argc, char *argv[]) {
  if (argc != 2) {
    return TEST_FAIL;
  }

  int test_case = atoi(argv[1]);

  switch (test_case) {

  // 0: Create an empty stack
  case 0: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    int result = (stack->top == NULL) ? TEST_PASS : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 1: Create a node
  case 1: {
    Node *node = create(5);

    if (node == NULL) {
      return TEST_FAIL;
    }

    int result =
        (node->value == 5 && node->next == NULL) ? TEST_PASS : TEST_FAIL;

    free(node);
    return result;
  }

  // 2: Push one element
  case 2: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);

    int result = (stack != NULL && length(stack) == 1 && stack->top != NULL &&
                  stack->top->value == 5 && stack->top->next == NULL)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 3: Push multiple elements
  case 3: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);
    stack = push(stack, 10);
    stack = push(stack, 15);

    int result =
        (stack != NULL && length(stack) == 3 && stack->top->value == 15 &&
         stack->top->next->value == 10 && stack->top->next->next->value == 5 &&
         stack->top->next->next->next == NULL)
            ? TEST_PASS
            : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 4: Peek at the top element
  case 4: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);
    stack = push(stack, 10);

    int result = (peek(stack) == 10) ? TEST_PASS : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 5: Peek does not remove an element
  case 5: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);
    stack = push(stack, 10);

    int first = peek(stack);
    int second = peek(stack);

    int result = (first == 10 && second == 10 && length(stack) == 2 &&
                  stack->top->value == 10)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 6: Pop one element
  case 6: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);

    int removed = pop(stack);

    int result = (removed == 5 && stack->top == NULL && length(stack) == 0)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 7: Pop multiple elements in LIFO order
  case 7: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);
    stack = push(stack, 10);
    stack = push(stack, 15);

    int first = pop(stack);
    int second = pop(stack);
    int third = pop(stack);

    int result = (first == 15 && second == 10 && third == 5 &&
                  length(stack) == 0 && stack->top == NULL)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 8: Pop the last element
  case 8: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);
    stack = push(stack, 10);

    pop(stack);
    int removed = pop(stack);

    int result = (removed == 5 && stack->top == NULL && length(stack) == 0)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 9: Push after the stack becomes empty
  case 9: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);
    pop(stack);

    stack = push(stack, 20);

    int result = (stack != NULL && length(stack) == 1 && stack->top != NULL &&
                  stack->top->value == 20 && stack->top->next == NULL)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 10: Length of an empty stack
  case 10: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    int result = (length(stack) == 0) ? TEST_PASS : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 11: Pop from an empty stack
  case 11: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    int result =
        (pop(stack) == -1 && stack->top == NULL) ? TEST_PASS : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 12: Peek at an empty stack
  case 12: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    int result = (peek(stack) == -1) ? TEST_PASS : TEST_FAIL;

    destroy(stack);
    return result;
  }

  // 13: Handle NULL arguments
  case 13: {
    int result = (push(NULL, 5) == NULL && pop(NULL) == -1 &&
                  peek(NULL) == -1 && length(NULL) == 0)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(NULL);
    return result;
  }

  // 14: Destroy an empty stack
  case 14: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    destroy(stack);
    return TEST_PASS;
  }

  // 15: Destroy a populated stack
  case 15: {
    Stack *stack = createStack();

    if (stack == NULL) {
      return TEST_FAIL;
    }

    stack = push(stack, 5);
    stack = push(stack, 10);
    stack = push(stack, 15);

    destroy(stack);
    return TEST_PASS;
  }

  default:
    return TEST_FAIL;
  }
}

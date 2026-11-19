#include <stdlib.h>

#ifndef QUEUE_TYPES_DEFINED
#define QUEUE_TYPES_DEFINED

typedef struct Node {
  int value;
  struct Node *next;
} Node;

typedef struct Queue {
  Node *head;
  Node *tail;
} Queue;

Queue *createQueue(void);
Node *create(int value);
Queue *enqueue(Queue *queue, int value);
int dequeue(Queue *queue);
int peek(Queue *queue);
int length(Queue *queue);
void destroy(Queue *queue);

#endif

enum TestResult { TEST_PASS = 0, TEST_FAIL = 1 };

int main(int argc, char *argv[]) {
  if (argc != 2) {
    return TEST_FAIL;
  }

  int test_case = atoi(argv[1]);

  switch (test_case) {

  // 0: Create an empty queue
  case 0: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    int result =
        (queue->head == NULL && queue->tail == NULL) ? TEST_PASS : TEST_FAIL;

    destroy(queue);
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

  // 2: Enqueue one element
  case 2: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);

    int result = (queue != NULL && length(queue) == 1 && queue->head != NULL &&
                  queue->tail != NULL && queue->head == queue->tail &&
                  queue->head->value == 5 && queue->head->next == NULL)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 3: Enqueue multiple elements
  case 3: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);
    queue = enqueue(queue, 10);
    queue = enqueue(queue, 15);

    int result = (queue != NULL && length(queue) == 3 &&
                  queue->head->value == 5 && queue->head->next->value == 10 &&
                  queue->tail->value == 15 && queue->tail->next == NULL)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 4: Peek at the first element
  case 4: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);
    queue = enqueue(queue, 10);

    int result = (peek(queue) == 5) ? TEST_PASS : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 5: Peek does not remove an element
  case 5: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);
    queue = enqueue(queue, 10);

    int first = peek(queue);
    int second = peek(queue);

    int result = (first == 5 && second == 5 && length(queue) == 2) ? TEST_PASS
                                                                   : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 6: Dequeue one element
  case 6: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);

    int removed = dequeue(queue);

    int result = (removed == 5 && queue->head == NULL && queue->tail == NULL &&
                  length(queue) == 0)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 7: Dequeue multiple elements in FIFO order
  case 7: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);
    queue = enqueue(queue, 10);
    queue = enqueue(queue, 15);

    int first = dequeue(queue);
    int second = dequeue(queue);
    int third = dequeue(queue);

    int result =
        (first == 5 && second == 10 && third == 15 && length(queue) == 0 &&
         queue->head == NULL && queue->tail == NULL)
            ? TEST_PASS
            : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 8: Dequeue the last element updates both pointers
  case 8: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);
    queue = enqueue(queue, 10);

    dequeue(queue);
    int removed = dequeue(queue);

    int result = (removed == 10 && queue->head == NULL && queue->tail == NULL)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 9: Enqueue after the queue becomes empty
  case 9: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);
    dequeue(queue);

    queue = enqueue(queue, 20);

    int result =
        (queue != NULL && length(queue) == 1 && queue->head == queue->tail &&
         queue->head->value == 20 && queue->tail->next == NULL)
            ? TEST_PASS
            : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 10: Length of an empty queue
  case 10: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    int result = (length(queue) == 0) ? TEST_PASS : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 11: Dequeue from an empty queue
  case 11: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    int result =
        (dequeue(queue) == -1 && queue->head == NULL && queue->tail == NULL)
            ? TEST_PASS
            : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 12: Peek at an empty queue
  case 12: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    int result = (peek(queue) == -1) ? TEST_PASS : TEST_FAIL;

    destroy(queue);
    return result;
  }

  // 13: Handle NULL arguments
  case 13: {
    int result = (enqueue(NULL, 5) == NULL && dequeue(NULL) == -1 &&
                  peek(NULL) == -1 && length(NULL) == 0)
                     ? TEST_PASS
                     : TEST_FAIL;

    destroy(NULL);
    return result;
  }

  // 14: Destroy an empty queue
  case 14: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    destroy(queue);
    return TEST_PASS;
  }

  // 15: Destroy a populated queue
  case 15: {
    Queue *queue = createQueue();

    if (queue == NULL) {
      return TEST_FAIL;
    }

    queue = enqueue(queue, 5);
    queue = enqueue(queue, 10);
    queue = enqueue(queue, 15);

    destroy(queue);
    return TEST_PASS;
  }

  default:
    return TEST_FAIL;
  }
}
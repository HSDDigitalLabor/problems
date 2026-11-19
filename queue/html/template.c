#include <stdio.h>
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

Queue *createQueue(void) {}

Node *create(int value) {}

Queue *enqueue(Queue *queue, int value) {}

int dequeue(Queue *queue) {}

int peek(Queue *queue) {}

int length(Queue *queue) {}

void destroy(Queue *queue) {}

int main(void) {}

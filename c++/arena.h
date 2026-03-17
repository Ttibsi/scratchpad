#ifndef ARENA_ALLOCATOR_H
#define ARENA_ALLOCATOR_H

#include <stddef.h>

typedef struct {
    // pointer arithmetic on void* isn't standard C
    unsigned char* memory;
    size_t capacity;
    size_t size;
} Arena;

static int   arenaInit(Arena* a, size_t capacity);
static void* arenaAlloc(Arena* a, size_t allocSize);
static void  arenaReset(Arena* a);
static void  arenaDestroy(Arena* a);

#endif

#ifdef ARENA_ALLOCATOR_IMPLEMENTATION
#include <stdlib.h>

static int arenaInit(Arena* a, size_t capacity) {
    if (!a || capacity == 0) { return 0; }

    a->memory = (unsigned char*)malloc(capacity);
    if (!a->memory) { return 0; }

    a->capacity = capacity;
    a->size = 0;

    return 1;
}

static void* arenaAlloc(Arena* a, size_t allocSize) {
    if (!a || allocSize == 0) { return NULL; }
    if (a->size + allocSize > a->capacity) { return NULL; }

    void* ptr = a->memory + a->size;
    a->size += allocSize;

    return ptr;
}

static void arenaReset(Arena* a) {
    if (!a) { return; }
    a->size = 0;
}

static void arenaDestroy(Arena* a) {
    if (!a) { return; }

    free(a->memory);
    a->memory = NULL;
    a->capacity = 0;
    a->size = 0;
}

#endif

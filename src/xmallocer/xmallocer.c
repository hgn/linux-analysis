#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct memory_tracker
{
    const char *component_name;
    size_t allocated_memory;
};

struct allocation_info
{
    void *ptr;
    const char *component_name;
    size_t size;
    struct allocation_info *next;
};

#define MAX_COMPONENTS 1024
static struct memory_tracker memory_trackers[MAX_COMPONENTS];
static size_t num_components = 0;

static struct allocation_info *allocations_head = NULL;

static struct memory_tracker *get_memory_tracker(const char *component)
{
    size_t i;
    for (i = 0; i < num_components; ++i) {
        if (strcmp(memory_trackers[i].component_name, component) == 0)
            return &memory_trackers[i];
    }
    if (num_components < MAX_COMPONENTS) {
        memory_trackers[num_components].component_name = component;
        memory_trackers[num_components].allocated_memory = 0;
        return &memory_trackers[num_components++];
    }
    return NULL;
}

static void track_allocation(void *ptr, const char *component, size_t size)
{
    struct allocation_info *new_allocation = (struct allocation_info *)malloc(sizeof(struct allocation_info));
    new_allocation->ptr = ptr;
    new_allocation->component_name = component;
    new_allocation->size = size;
    new_allocation->next = allocations_head;
    allocations_head = new_allocation;
}

static void untrack_allocation(void *ptr)
{
    struct allocation_info **current = &allocations_head;
    while (*current) {
        if ((*current)->ptr == ptr) {
            struct allocation_info *to_remove = *current;
            *current = to_remove->next;

            struct memory_tracker *tracker = get_memory_tracker(to_remove->component_name);
            if (tracker)
                tracker->allocated_memory -= to_remove->size;

            free(to_remove);
            return;
        }
        current = &(*current)->next;
    }
}

void clean_memory_tracker()
{
    struct allocation_info *current = allocations_head;
    while (current) {
        struct allocation_info *to_remove = current;
        current = current->next;

        struct memory_tracker *tracker = get_memory_tracker(to_remove->component_name);
        if (tracker)
            tracker->allocated_memory -= to_remove->size;

        free(to_remove->ptr);
        free(to_remove);
    }
    allocations_head = NULL;
    num_components = 0;
}

#define XMALLOC(component, size) ({ \
    void *ptr = malloc(size); \
    if (ptr) { \
        struct memory_tracker *tracker = get_memory_tracker(component); \
        if (tracker) \
            tracker->allocated_memory += size; \
        track_allocation(ptr, component, size); \
    } \
    ptr; \
})

#define XFREE(ptr) do { \
    if (ptr) { \
        untrack_allocation(ptr); \
        free(ptr); \
    } \
} while (0)

void print_memory_usage()
{
    size_t i;
    printf("Memory usage per component:\n");
    for (i = 0; i < num_components; ++i) {
        printf("Component: %s, Allocated Memory: %zu bytes\n", 
               memory_trackers[i].component_name, 
               memory_trackers[i].allocated_memory);
    }
}

__attribute__((destructor)) void finalize()
{
    clean_memory_tracker();
}

int main()
{
    char *ptr1 = XMALLOC("SubsystemA", 128);
    char *ptr2 = XMALLOC("SubsystemA", 128);
    char *ptr3 = XMALLOC("SubsystemB", 256);

    print_memory_usage();

    XFREE(ptr1);
    XFREE(ptr2);
    XFREE(ptr3);

    print_memory_usage();

    return 0;
}


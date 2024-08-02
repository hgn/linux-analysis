#include <stdio.h>

int main() {
    volatile int src = 42;
    volatile int dst = 0;

    asm volatile (
        "movq $0, %%rcx\n\t"
        "movq $100000000000, %%rdx\n\t"
        "loop_start:\n\t"
        "movl %1, %%eax\n\t"
        "movl %%eax, %0\n\t"
        "incq %%rcx\n\t"
        "cmpq %%rdx, %%rcx\n\t"
        "jne loop_start\n\t"
        : "=m" (dst)
        : "m" (src)
        : "eax", "rcx", "rdx"
    );

    return 0;
}

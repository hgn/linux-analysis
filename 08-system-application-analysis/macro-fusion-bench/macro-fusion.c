#include <x86intrin.h>
#include <stdint.h>
#include <stdio.h>

#ifdef LIKWID
#include <likwid.h>
#define MEASURE_INIT()                                          \
    do {                                                        \
        likwid_markerInit();                                    \
        likwid_markerThreadInit();                              \
    } while (0)
#define MEASURE_FINI()                                          \
    do {                                                        \
        likwid_markerClose();                                   \
    } while (0)
#define MEASURE(name, code)                                     \
    do {                                                        \
        sum1 = sum2 = 0;                                        \
        likwid_markerStartRegion(name);                         \
        code;                                                   \
        likwid_markerStopRegion(name);                          \
        printf("%s: sum1=%ld, sum2=%ld\n", name, sum1, sum2);   \
    } while (0)
#else // not LIKWID
#define MEASURE_INIT()
#define MEASURE_FINI()
#define MEASURE(name, code)                                     \
    do {                                                        \
        sum1 = sum2 = 0;                                        \
        code;                                                   \
        printf("%s: sum1=%ld, sum2=%ld\n", name, sum1, sum2);   \
    } while (0)
#endif // not LIKWID


#define ASM_TWO_MICRO_TWO_MACRO(in1, sum1, in2, sum2, max)      \
    __asm volatile ("1:\n"                                      \
                    "add (%[IN1]), %[SUM1]\n"                   \
                    "cmp %[MAX], %[SUM1]\n"                     \
                    "jae 2f\n"                                  \
                    "add (%[IN2]), %[SUM2]\n"                   \
                    "cmp %[MAX], %[SUM2]\n"                     \
                    "jb 1b\n"                                   \
                    "2:" :                                      \
                    [SUM1] "+&r" (sum1),                        \
                    [SUM2] "+&r" (sum2) :                       \
                    [IN1] "r" (in1),                            \
                    [IN2] "r" (in2),                            \
                    [MAX] "r" (max))

#define ASM_NO_MICRO_TWO_MACRO(in1, sum1, in2, sum2, max, tmp1, tmp2)   \
    __asm volatile ("1:\n"                                      \
                    "mov (%[IN1]), %[TMP1]\n"                   \
                    "add %[TMP1], %[SUM1]\n"                    \
                    "cmp %[MAX], %[SUM1]\n"                     \
                    "jae 2f\n"                                  \
                    "mov (%[IN2]), %[TMP2]\n"                   \
                    "add %[TMP2], %[SUM2]\n"                    \
                    "cmp %[MAX], %[SUM2]\n"                     \
                    "jb 1b\n"                                   \
                    "2:" :                                      \
                    [TMP1] "=&r" (tmp1),                        \
                    [TMP2] "=&r" (tmp2),                        \
                    [SUM1] "+&r" (sum1),                        \
                    [SUM2] "+&r" (sum2) :                       \
                    [IN1] "r" (in1),                            \
                    [IN2] "r" (in2),                            \
                    [MAX] "r" (max))


#define ASM_ONE_MICRO_TWO_MACRO(in1, sum1, in2, sum2, max, tmp) \
    __asm volatile ("1:\n"                                      \
                    "add (%[IN1]), %[SUM1]\n"                   \
                    "cmp %[MAX], %[SUM1]\n"                     \
                    "jae 2f\n"                                  \
                    "mov (%[IN2]), %[TMP]\n"                    \
                    "add %[TMP], %[SUM2]\n"                     \
                    "cmp %[MAX], %[SUM2]\n"                     \
                    "jb 1b\n"                                   \
                    "2:" :                                      \
                    [TMP] "=&r" (tmp),                          \
                    [SUM1] "+&r" (sum1),                        \
                    [SUM2] "+&r" (sum2) :                       \
                    [IN1] "r" (in1),                            \
                    [IN2] "r" (in2),                            \
                    [MAX] "r" (max))


#define ASM_ONE_MICRO_ONE_MACRO(in1, sum1, in2, sum2, max, tmp) \
    __asm volatile ("1:\n"                                      \
                    "add (%[IN1]), %[SUM1]\n"                   \
                    "cmp %[MAX], %[SUM1]\n"                     \
                    "mov (%[IN1]), %[TMP]\n"                    \
                    "jae 2f\n"                                  \
                    "add %[TMP], %[SUM2]\n"                     \
                    "cmp %[MAX], %[SUM2]\n"                     \
                    "jb 1b\n"                                   \
                    "2:" :                                      \
                    [TMP] "=&r" (tmp),                          \
                    [SUM1] "+&r" (sum1),                        \
                    [SUM2] "+&r" (sum2) :                       \
                    [IN1] "r" (in1),                            \
                    [IN2] "r" (in2),                            \
                    [MAX] "r" (max))

// two separate loads and adds, two non-fused cmp then jcc
#define ASM_NO_MICRO_NO_MACRO(in1, sum1, in2, sum2, max, tmp1, tmp2)    \
    __asm volatile ("mov (%[IN1]), %[TMP1]\n"                   \
                    "1:\n"                                      \
                    "add %[TMP1], %[SUM1]\n"                    \
                    "cmp %[MAX], %[SUM1]\n"                     \
                    "mov (%[IN2]), %[TMP2]\n"                   \
                    "jae 2f\n"                                  \
                    "add %[TMP2], %[SUM2]\n"                    \
                    "cmp %[MAX], %[SUM2]\n"                     \
                    "mov (%[IN1]), %[TMP1]\n"                   \
                    "jb 1b\n"                                   \
                    "2:" :                                      \
                    [TMP1] "=&r" (tmp1),                        \
                    [TMP2] "=&r" (tmp2),                        \
                    [SUM1] "+&r" (sum1),                        \
                    [SUM2] "+&r" (sum2) :                       \
                    [IN1] "r" (in1),                            \
                    [IN2] "r" (in2),                            \
                    [MAX] "r" (max))


int main(int argc, char **argv) {
	uint64_t tmp, tmp1, tmp2;
	uint64_t sum1, sum2;
	uint64_t in1 = 1;
	uint64_t in2 = 1;
	uint64_t max = 10000000;

	(void) argc; (void) argv;

	MEASURE_INIT();

	MEASURE("two_micro_two_macro", ASM_TWO_MICRO_TWO_MACRO(&in1, sum1, &in2, sum2, max));
	MEASURE("one_micro_two_macro", ASM_ONE_MICRO_TWO_MACRO(&in1, sum1, &in2, sum2, max, tmp));
	MEASURE("one_micro_one_macro", ASM_ONE_MICRO_ONE_MACRO(&in1, sum1, &in2, sum2, max, tmp));
	MEASURE("no_micro_two_macro", ASM_NO_MICRO_TWO_MACRO(&in1, sum1, &in2, sum2, max, tmp1, tmp2));
	MEASURE("no_micro_no_macro", ASM_NO_MICRO_NO_MACRO(&in1, sum1, &in2, sum2, max, tmp1, tmp2));

	MEASURE_FINI();


	return 0;
}


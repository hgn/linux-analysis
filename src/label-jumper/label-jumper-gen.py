#!/usr/bin/env python3

import argparse
import sys
import textwrap

# Configuration for the generated C code
NUM_LABELS = 10000

# generate_sparse_values function is no longer needed

def generate_c_code_computed_goto(num_labels):
    """Generates C code using computed gotos and a FAST_RAND32 PRNG macro."""
    print(f"Generating C code with {num_labels} labels and computed gotos...", file=sys.stderr)

    # --- C Code Template ---
    c_code = textwrap.dedent(f"""\
    #include <stdio.h>
    #include <stdlib.h>
    #include <time.h>
    #include <unistd.h>
    #include <stdbool.h>
    #include <errno.h>
    #include <limits.h>
    #include <stdint.h> // Needed for uint32_t

    #define NUM_LABELS {num_labels}

    // Simple, branchless XORshift32 PRNG macro with counter XOR
    // Input: 'state' variable (uint32_t, must be non-zero), 'counter' variable (unsigned int)
    // Output: Updated 'state' (in place), the expression's value is the new state XOR counter (random number)
    #define FAST_RAND32_EXTENDED(state, counter) \\
        ( (state) ^= ((state) << 13), \\
          (state) ^= ((state) >> 17), \\
          (state) ^= ((state) << 5), \\
          (state) ^ (counter)          )

    int main(int argc, char *argv[]) {{
        long limit_arg_long;
        int limit_arg;
        int effective_num_labels;
        char *endptr;
        unsigned int counter = 0; // Counter for extended PRNG

        // --- Argument Parsing ---
        if (argc != 2) {{
            fprintf(stderr, "Usage: %s <limit>\\n", argv[0]);
            fprintf(stderr, "  limit: Max number of labels to target (1 to %d), or 0 for all labels.\\n", NUM_LABELS);
            return EXIT_FAILURE;
        }}

        errno = 0;
        limit_arg_long = strtol(argv[1], &endptr, 10);

        if (endptr == argv[1] || *endptr != '\\0' || errno == ERANGE || limit_arg_long < 0 || limit_arg_long > INT_MAX) {{
            fprintf(stderr, "Error: Invalid or out-of-range limit value '%s' (must be 0 to %d)\\n", argv[1], INT_MAX);
            return EXIT_FAILURE;
        }}
         if (limit_arg_long < 0) {{
            fprintf(stderr, "Error: Limit value %ld cannot be negative.\\n", limit_arg_long);
            return EXIT_FAILURE;
        }}

        limit_arg = (int)limit_arg_long;

        if (limit_arg == 0) {{
            effective_num_labels = NUM_LABELS;
            printf("Info: Limit is 0. Targeting all %d defined labels.\\n", NUM_LABELS);
        }} else if (limit_arg > NUM_LABELS) {{
            fprintf(stderr, "Warning: Limit %d exceeds total labels %d. Clamping to %d.\\n", limit_arg, NUM_LABELS, NUM_LABELS);
            effective_num_labels = NUM_LABELS;
        }} else {{
            effective_num_labels = limit_arg;
            printf("Info: Targeting first %d defined labels (Indices 0 to %d).\\n", effective_num_labels, effective_num_labels - 1);
        }}

        if (effective_num_labels <= 0) {{
             fprintf(stderr, "Error: Effective number of labels (%d) must be positive.\\n", effective_num_labels);
             return EXIT_FAILURE;
        }}

        // --- Computed Goto Setup (Requires GCC 'labels as values') ---
    #if defined(__GNUC__) && !defined(__clang__)

        static const void* label_targets[NUM_LABELS] = {{
    """) # End of initial C code block

    # --- Generate the array initializer with label addresses ---
    label_refs = []
    print(f"Generating {num_labels} label references for array...", file=sys.stderr)
    for i in range(num_labels):
        label_refs.append(f"        &&TARGET_LABEL_{i}")
    c_code += ",\n".join(label_refs) + "\n    };\n\n"

    # --- Add variables and setup for the jump loop ---
    c_code += textwrap.dedent(f"""\
        void *next_target;
        int random_index;
        uint32_t rng_state; // State for the FAST_RAND32 PRNG macro

        // Seed the PRNG state. Must not be zero.
        // Using time and PID for better initial randomness per run.
        rng_state = (uint32_t)time(NULL) ^ (uint32_t)getpid();
        if (rng_state == 0) {{
            rng_state = 0xBAD5EED; // Use an arbitrary non-zero value if seed is 0
        }}

        // --- Initial Jump ---
        // Use the PRNG macro instead of rand()
        random_index = FAST_RAND32_EXTENDED(rng_state, counter) % effective_num_labels;
        next_target = (void*)label_targets[random_index];

        printf("Starting infinite random jump loop (PID: %d)...\\n", getpid());
        printf("Using FAST_RAND32_EXTENDED PRNG macro with counter XOR.\\n"); // Indicate macro usage
        printf("Press Ctrl+C to stop.\\n");

        goto *next_target;


        // --- Generated Labels and Jump Logic ---
    """) # End of setup block

    # --- Generate the label blocks ---
    print(f"Generating {num_labels} label blocks using FAST_RAND32_EXTENDED...", file=sys.stderr)
    label_blocks = []
    for i in range(num_labels):
        label_block = f"    TARGET_LABEL_{i}:\n"
        # Use PRNG Macro to calculate next random index
        label_block += f"        random_index = FAST_RAND32_EXTENDED(rng_state, counter) % effective_num_labels;\n"
        label_block += f"        next_target = (void*)label_targets[random_index];\n"
        label_block += f"        __asm__ __volatile__(\"nop\");\n" # Keep nop
        label_block += f"        counter++; // Increment counter in each label block\n"
        label_block += f"        goto *next_target;\n"
        label_blocks.append(label_block)
    c_code += "\n".join(label_blocks) + "\n"

    # --- Add closing parts and non-GCC fallback ---
    c_code += textwrap.dedent(f"""\

        // Unreachable code
        printf("Error: Reached theoretically unreachable code!\\n");
        return 1;

    #else
        fprintf(stderr, "Error: This program requires GCC's 'labels as values' extension.\\n");
        fprintf(stderr, "Compile this code with GCC.\\n");
        return EXIT_FAILURE;
    #endif // __GNUC__ && !__clang__

    }} // end of main
    """) # End of final C code block

    print("C code generation complete.", file=sys.stderr)
    return c_code

# --- Skriptausführung ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generiert C-Code mit zufälligen computed gotos (benötigt GCC).",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILENAME",
        default=None,
        help="Name der C-Ausgabedatei (Standard: stdout)"
    )

    args = parser.parse_args()

    generated_c_code = generate_c_code_computed_goto(NUM_LABELS)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(generated_c_code)
            print(f"C code written to '{args.output}'", file=sys.stderr)
        except IOError as e:
            print(f"Fehler beim Schreiben der Datei '{args.output}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(generated_c_code)

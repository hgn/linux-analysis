message:
        .ascii  "Howdy world\n"
        .global _start
        .text
_start:
				#  rax -> syscall write(1)
        mov     $1, %rax
				# rdi -> file handler, 1 == STDOUT_FILENO
        mov     $1, %rdi
        mov     $message, %rsi
        mov     $12, %rdx
        syscall

        # exit(0)
        mov     $60, %rax
        xor     %rdi, %rdi
        syscall


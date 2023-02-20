
void lea_loop(void)
{
	while (1) {
		__asm__ volatile("# LLVM-MCA-BEGIN leal");
		__asm__ __volatile__(
			"leal 1(%eax), %eax\n\n"
			"leal 1(%ebx), %ebx");
		__asm__ volatile("# LLVM-MCA-END");
	}
}

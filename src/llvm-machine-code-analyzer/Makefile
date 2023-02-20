

analyze: analyze_mca

analyze_mca:
	clang array-add.c -O1 -S -o - | llvm-mca-15 -mcpu=skylake -bottleneck-analysis -timeline


analyze_iaca:
	clang --target=x86_64-pc-linux-gnu -mtune=skylake -O1 -c -o array-add.o array-add.c


all: analyze

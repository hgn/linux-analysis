CC = gcc

.PHONY: clean run all

all: main-lazy main-relro

main-relro: main.c
	$(CC) -O0 -o main-relro -Wl,-z,relro,-z,now main.c

main-lazy: main.c
	$(CC) -O0 -o main-lazy  -Wl,-z,norelro main.c 

run: main
	@echo 'sudo bash -c "echo 0 > /proc/sys/kernel/randomize_va_space"'
	@echo "lazy:"
	./main-lazy > map-lazy.txt
	readelf -d ./main-lazy | grep BIND_NOW - || true
	objdump -R ./main-lazy | grep system@ -
	readelf -W -l ./main-lazy | grep GNU_RELRO || true
	readelf -l ./main-lazy 2> /dev/null | grep '\.got\.plt'
	checksec --file=./main-lazy
	@echo "relro:"
	./main-relro > map-relro.txt
	readelf -d ./main-relro | grep BIND_NOW - || true
	objdump -R ./main-relro | grep system@ -
	readelf -W -l ./main-relro | grep GNU_RELRO || true
	readelf -l ./main-relro 2> /dev/null | grep '\.got\.plt' || true
	checksec --file=./main-relro
	@echo "nvim -d map-lazy.txt map-relro.txt" 

clean:
	rm -f *.o main-lazy main-relro *.txt main

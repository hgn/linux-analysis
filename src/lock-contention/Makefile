OBJ     = lock-contention
CFLAGS  = -g -fno-omit-frame-pointer -O0 -Wall 
LDFLAGS = -lm -pthread

OBJ_C   = $(addsuffix .c, $(OBJ))

.PHONY: all collect analyze clean distclean build

all: preprocess analyze

$(OBJ): $(OBJ_C)
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)


build: $(OBJ)

collect: build
	sudo perf record -e syscalls:sys_enter_futex,syscalls:sys_exit_futex -- ./$(OBJ) 

analyze:
	sudo perf script report futex-contention
	sudo perf script -F tid,time,cpu,event,trace,ip | head

clean:
	rm -rf *.data *.data.old *.raw *.txt

disclean: clean
	rm -f $(OBJ)


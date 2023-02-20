CC = gcc
CFLAGS = -O2 -Wall
LFLAGS = -lm

all:	rapl-plot

rapl-plot:	rapl-plot.o
	$(CC) -o rapl-plot rapl-plot.o $(LFLAGS)

rapl-plot.o:	rapl-plot.c
	$(CC) $(CFLAGS) -c rapl-plot.c

clean:	
	rm -f *.o *~ rapl-plot *.csv

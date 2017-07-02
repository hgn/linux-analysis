

CFLAGS := -Wall -Wextra

all: howdy-world howdy-world.i

howdy-world.i: howdy-world.c
	$(CC) -E $< -o $@

howdy-world: howdy-world.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf howdy-world howdy-world.i
